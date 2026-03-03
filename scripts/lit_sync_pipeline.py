from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from collatz.literature import (
    ZoteroClient,
    bib_entry_to_zotero_item,
    download_first_pdf,
    parse_bibtex_entries,
    validate_entry,
    write_knowledge_note,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate BibTeX entries, sync to Zotero group library, download available PDFs, "
            "and build skill knowledge notes."
        )
    )
    parser.add_argument("--bib", type=Path, default=Path("paper/refs.bib"), help="Input BibTeX file path.")
    parser.add_argument(
        "--skill-references-dir",
        type=Path,
        default=Path("docs/literature/skill_knowledge"),
        help="Folder where PDFs and notes are created.",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
        default=Path("analysis/results/literature_sync_report.json"),
        help="Output JSON report path.",
    )
    parser.add_argument(
        "--download-pdfs",
        action="store_true",
        help="Try downloading available PDFs to the skill references folder.",
    )
    parser.add_argument(
        "--sync-zotero",
        action="store_true",
        help="Create Zotero items in an existing group library.",
    )
    parser.add_argument("--zotero-user-id", default="", help="Zotero user ID used to discover groups by name.")
    parser.add_argument("--zotero-group-id", default="", help="Target Zotero group ID.")
    parser.add_argument(
        "--zotero-group-name",
        default="",
        help="Target Zotero group name (requires --zotero-user-id).",
    )
    parser.add_argument(
        "--zotero-api-key-env",
        default="ZOTERO_API_KEY",
        help="Environment variable that stores the Zotero API key.",
    )
    parser.add_argument(
        "--run-external-checks",
        action="store_true",
        help="Run external BibTeX checkers (bibtex-tidy by default) and store their output in the report.",
    )
    parser.add_argument(
        "--external-checker-bin",
        default="npx",
        help="Executable used to run the external checker.",
    )
    parser.add_argument(
        "--external-checker-package",
        default="bibtex-tidy",
        help="Package name passed to npx.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 2 if validation errors are present, or code 3 if warnings are present.",
    )
    return parser.parse_args()


def _resolve_group_id(client: ZoteroClient, args: argparse.Namespace) -> str:
    if args.zotero_group_id:
        return args.zotero_group_id
    if not args.zotero_group_name:
        raise ValueError("Missing Zotero target: provide --zotero-group-id or --zotero-group-name.")
    found = client.find_group_id_by_name(args.zotero_group_name)
    if found:
        return found
    raise ValueError(
        "Zotero group was not found by name. Create the group once in Zotero UI, then rerun this script."
    )


def main() -> int:
    args = parse_args()
    if not args.bib.exists():
        raise FileNotFoundError(f"BibTeX file not found: {args.bib}")

    bib_text = args.bib.read_text(encoding="utf-8")
    entries = parse_bibtex_entries(bib_text)

    refs_dir = args.skill_references_dir
    pdf_dir = refs_dir / "pdfs"
    notes_dir = refs_dir / "notes"
    args.report_json.parent.mkdir(parents=True, exist_ok=True)
    refs_dir.mkdir(parents=True, exist_ok=True)

    validations = [validate_entry(entry) for entry in entries]
    validation_by_key = {item.key: item for item in validations}

    external_checks: list[dict[str, object]] = []
    if args.run_external_checks:
        checker_bin = args.external_checker_bin
        if os.name == "nt" and checker_bin == "npx":
            powershell_exe = r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe"
            cmd = [
                powershell_exe,
                "-NoProfile",
                "-Command",
                (
                    f'npx -y {args.external_checker_package} "{args.bib}" '
                    "--no-modify"
                ),
            ]
        else:
            cmd = [
                checker_bin,
                "-y",
                args.external_checker_package,
                str(args.bib),
                "--no-modify",
            ]
        try:
            run = subprocess.run(cmd, capture_output=True, text=True, check=False)
            external_checks.append(
                {
                    "name": "bibtex-tidy-parse",
                    "command": cmd,
                    "returncode": run.returncode,
                    "stdout": run.stdout,
                    "stderr": run.stderr,
                }
            )
        except FileNotFoundError as exc:
            external_checks.append(
                {
                    "name": "bibtex-tidy-parse",
                    "command": cmd,
                    "returncode": None,
                    "stdout": "",
                    "stderr": f"external_checker_not_found:{exc}",
                }
            )

    downloaded_pdfs: dict[str, str] = {}
    if args.download_pdfs:
        for entry in entries:
            pdf_path = download_first_pdf(entry, pdf_dir)
            if pdf_path:
                downloaded_pdfs[entry.key] = str(pdf_path)

    note_paths: dict[str, str] = {}
    for entry in entries:
        note_path = write_knowledge_note(
            entry=entry,
            validation=validation_by_key[entry.key],
            pdf_path=Path(downloaded_pdfs[entry.key]) if entry.key in downloaded_pdfs else None,
            output_dir=notes_dir,
        )
        note_paths[entry.key] = str(note_path)

    zotero_response: dict[str, object] = {"enabled": args.sync_zotero, "status": "skipped"}
    if args.sync_zotero:
        api_key = os.getenv(args.zotero_api_key_env, "").strip()
        if not api_key:
            raise ValueError(f"Missing Zotero API key env var: {args.zotero_api_key_env}")
        if not args.zotero_user_id:
            raise ValueError("--zotero-user-id is required for --sync-zotero")
        client = ZoteroClient(user_id=args.zotero_user_id, api_key=api_key)
        group_id = _resolve_group_id(client, args)
        collection_result = client.create_collection(group_id, "Collatz Literature Sync")
        create_result = client.create_items(group_id, [bib_entry_to_zotero_item(entry) for entry in entries])
        zotero_response = {
            "enabled": True,
            "status": "ok",
            "group_id": group_id,
            "collection_result": collection_result,
            "create_items_result": create_result,
        }

    report = {
        "bib_path": str(args.bib),
        "entry_count": len(entries),
        "validated_ok": sum(1 for item in validations if item.status == "ok"),
        "validated_warning": sum(1 for item in validations if item.status == "warning"),
        "validated_error": sum(1 for item in validations if item.status == "error"),
        "downloaded_pdf_count": len(downloaded_pdfs),
        "downloaded_pdfs": downloaded_pdfs,
        "knowledge_notes": note_paths,
        "validation": [item.__dict__ for item in validations],
        "zotero": zotero_response,
        "external_checks": external_checks,
    }
    args.report_json.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Wrote report: {args.report_json}")
    print(f"Entries: {len(entries)}, PDFs: {len(downloaded_pdfs)}")
    if args.strict:
        if report["validated_error"] > 0:
            print("Strict mode failed: validation errors present.")
            return 2
        if report["validated_warning"] > 0:
            print("Strict mode failed: validation warnings present.")
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
