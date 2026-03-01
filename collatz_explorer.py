#!/usr/bin/env python3
"""collatz_explorer.py

Small CLI tool to explore the Collatz conjecture:
- Show the full sequence for a starting value.
- Measure stopping time (steps to reach 1) and peak value.
- Analyze all starts from 1..N to spot interesting patterns.

This script is a thin CLI layer. The canonical implementation is in `src/collatz/`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running without installing the package.
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if SRC.exists() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from collatz.core import collatz_sequence  # noqa: E402
from collatz.stats import analyze_range  # noqa: E402


def print_sequence_report(start: int, max_steps: int) -> None:
    seq = collatz_sequence(start, max_steps=max_steps)
    reached_one = seq[-1] == 1
    steps = len(seq) - 1
    peak = max(seq)

    print(f"Start value: {start}")
    print(f"Reached 1: {'yes' if reached_one else 'no'}")
    print(f"Steps taken: {steps}")
    print(f"Peak value:  {peak}")
    print("Sequence:")
    print(" -> ".join(str(x) for x in seq))


def print_range_report(limit: int, max_steps: int) -> None:
    stats = analyze_range(limit, max_steps=max_steps)
    print(f"Range analyzed: 1..{stats['limit']}")
    print(f"Longest stopping time: start={stats['max_time_start']}, steps={stats['max_time']}")
    print(f"Highest peak reached:  start={stats['max_peak_start']}, peak={stats['max_peak']}")
    print(f"Unresolved within max_steps={max_steps}: {stats['unresolved']}")
    print("")
    print("Stopping time distribution (bucketed by 10 steps):")
    for bucket_start, count in stats["time_buckets"].items():
        bar = "#" * min(int(count), 60)
        print(f"{bucket_start:>3}-{bucket_start+9:>3}: {count:>5} {bar}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Explore Collatz sequences for a start value or a range."
    )
    parser.add_argument(
        "--start",
        type=int,
        default=27,
        help="Starting value for sequence view (default: 27).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Upper bound for range analysis 1..limit (default: 100).",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=10000,
        help="Safety cap for generated steps (default: 10000).",
    )
    parser.add_argument(
        "--mode",
        choices=["sequence", "range", "both"],
        default="both",
        help="What to print (default: both).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.mode in ("sequence", "both"):
        print_sequence_report(args.start, args.max_steps)
    if args.mode == "both":
        print("\n" + "=" * 72 + "\n")
    if args.mode in ("range", "both"):
        print_range_report(args.limit, args.max_steps)


if __name__ == "__main__":
    main()
