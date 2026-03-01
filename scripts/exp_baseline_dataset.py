#!/usr/bin/env python3
"""Generate a baseline dataset for Collatz range statistics.

Outputs a CSV with columns:
  start, stopping_time, peak

Usage:
  python scripts/exp_baseline_dataset.py --limit 100000 --out analysis/results/baseline_100k.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from collatz.core import collatz_sequence  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=1000)
    p.add_argument("--max-steps", type=int, default=10000)
    p.add_argument("--out", type=str, default="analysis/results/baseline.csv")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["start", "stopping_time", "peak"])

        for n in range(1, args.limit + 1):
            seq = collatz_sequence(n, max_steps=args.max_steps)
            if seq[-1] != 1:
                # Keep unresolved sequences out of the baseline dataset.
                continue
            writer.writerow([n, len(seq) - 1, max(seq)])

            if n % max(1, args.limit // 10) == 0:
                print(f"... {n}/{args.limit}")

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
