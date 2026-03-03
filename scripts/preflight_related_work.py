from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preflight gate for related-work and bibliography edits."
    )
    parser.add_argument("--bib", default="paper/refs.bib", help="Path to BibTeX file.")
    parser.add_argument(
        "--report-json",
        default="analysis/results/literature_sync_report.json",
        help="Path for the generated report.",
    )
    parser.add_argument(
        "--run-external-checks",
        action="store_true",
        help="Run external checker (bibtex-tidy) in addition to DOI/arXiv validation.",
    )
    args = parser.parse_args()

    script = Path("scripts/lit_sync_pipeline.py")
    if not script.exists():
        print("ERROR: missing scripts/lit_sync_pipeline.py", file=sys.stderr)
        return 2

    cmd = [
        sys.executable,
        str(script),
        "--bib",
        args.bib,
        "--report-json",
        args.report_json,
        "--strict",
    ]
    if args.run_external_checks:
        cmd.append("--run-external-checks")

    print("=== Bibliography preflight gate ===")
    print("Command:", " ".join(cmd))
    proc = subprocess.run(cmd)
    print("Exit code:", proc.returncode)
    print("Report:", args.report_json)
    if proc.returncode != 0:
        print("GATE FAILED: fix bibliography issues before editing related work.", file=sys.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
