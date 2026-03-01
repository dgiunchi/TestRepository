#!/usr/bin/env python3
"""
collatz_explorer.py

Small CLI tool to explore the Collatz conjecture:
- Show the full sequence for a starting value.
- Measure stopping time (steps to reach 1) and peak value.
- Analyze all starts from 1..N to spot interesting patterns.
"""

from __future__ import annotations

import argparse
from collections import Counter


def collatz_next(n: int) -> int:
    """Return the next Collatz value."""
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def collatz_sequence(start: int, max_steps: int = 10000) -> list[int]:
    """Generate Collatz sequence from start until 1 (or max_steps)."""
    if start < 1:
        raise ValueError("start must be >= 1")

    seq = [start]
    n = start
    steps = 0
    while n != 1 and steps < max_steps:
        n = collatz_next(n)
        seq.append(n)
        steps += 1
    return seq


def stopping_time(start: int, max_steps: int = 10000) -> int | None:
    """
    Return number of steps required to reach 1.
    Returns None if max_steps is reached first.
    """
    seq = collatz_sequence(start, max_steps=max_steps)
    if seq[-1] != 1:
        return None
    return len(seq) - 1


def analyze_range(limit: int, max_steps: int = 10000) -> dict[str, object]:
    """Analyze starts 1..limit and return summary statistics."""
    if limit < 1:
        raise ValueError("limit must be >= 1")

    max_time_start = 1
    max_time = 0
    max_peak_start = 1
    max_peak = 1
    unresolved = 0
    time_buckets: Counter[int] = Counter()

    for start in range(1, limit + 1):
        seq = collatz_sequence(start, max_steps=max_steps)
        if seq[-1] != 1:
            unresolved += 1
            continue

        time = len(seq) - 1
        peak = max(seq)

        if time > max_time:
            max_time = time
            max_time_start = start

        if peak > max_peak:
            max_peak = peak
            max_peak_start = start

        # Bucket stopping times into ranges of width 10 for quick pattern reading.
        bucket = (time // 10) * 10
        time_buckets[bucket] += 1

    return {
        "limit": limit,
        "max_time_start": max_time_start,
        "max_time": max_time,
        "max_peak_start": max_peak_start,
        "max_peak": max_peak,
        "unresolved": unresolved,
        "time_buckets": dict(sorted(time_buckets.items())),
    }


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
        bar = "#" * min(count, 60)
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
