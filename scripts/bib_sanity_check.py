from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from collatz.literature import parse_bibtex_entries


REQUIRED_FIELDS: dict[str, set[str]] = {
    "article": {"author", "title", "year"},
    "inproceedings": {"author", "title", "booktitle", "year"},
    "book": {"author", "title", "publisher", "year"},
    "misc": {"title"},
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run quick BibTeX sanity checks (stdlib + project parser).")
    parser.add_argument("--bib", default="paper/refs.bib", help="Input BibTeX file.")
    args = parser.parse_args()

    bib_path = Path(args.bib)
    if not bib_path.exists():
        raise FileNotFoundError(f"BibTeX file not found: {bib_path}")

    entries = parse_bibtex_entries(bib_path.read_text(encoding="utf-8"))
    problems: list[str] = []
    for entry in entries:
        required = REQUIRED_FIELDS.get(entry.entry_type, {"author", "title", "year"})
        missing = sorted([name for name in required if not entry.fields.get(name)])
        if missing:
            problems.append(f"- {entry.key} ({entry.entry_type}): missing {', '.join(missing)}")

    if problems:
        print("BibTeX sanity check: FOUND ISSUES")
        print("\n".join(problems))
        return 2

    print("BibTeX sanity check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
