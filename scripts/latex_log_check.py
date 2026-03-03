from __future__ import annotations

import argparse
import re
from pathlib import Path

PATTERNS = [
    ("ERROR", re.compile(r"^!\s+(.+)$")),
    ("UNDEF_REF", re.compile(r"LaTeX Warning: Reference .* undefined")),
    ("UNDEF_CITE", re.compile(r"LaTeX Warning: Citation .* undefined")),
    ("OVERFULL", re.compile(r"Overfull \\hbox .*")),
    ("UNDERFULL", re.compile(r"Underfull \\hbox .*")),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract common warnings/errors from a LaTeX log.")
    parser.add_argument("--log", default="paper/build/main.log", help="Path to LaTeX .log file.")
    args = parser.parse_args()

    log_path = Path(args.log)
    if not log_path.exists():
        print(f"LaTeX log not found: {log_path}")
        return 1

    findings: list[tuple[str, str]] = []
    for line in log_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        for tag, pattern in PATTERNS:
            if pattern.search(stripped):
                findings.append((tag, stripped))
                break

    if not findings:
        print("No common warnings/errors found.")
        return 0

    print("LaTeX log findings:")
    for tag, line in findings[:300]:
        print(f"[{tag}] {line}")
    if len(findings) > 300:
        print(f"... ({len(findings) - 300} more)")

    return 2 if any(tag == "ERROR" for tag, _ in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
