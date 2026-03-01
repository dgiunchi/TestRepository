#!/usr/bin/env python3
"""Scan generalized Collatz-like rules and summarize behavior.

Rule form:
  if n % divisor == 0: n <- n // divisor
  else:                n <- multiplier * n + increment

Examples:
  python scripts/exp_generalized_rule_scan.py --limit 5000
  python scripts/exp_generalized_rule_scan.py --limit 3000 --rules "2:3:1,3:5:1,5:7:1"
"""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from collatz.experiments import generalized_next  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=5000)
    p.add_argument("--max-steps", type=int, default=500)
    p.add_argument("--stop-at", type=int, default=1)
    p.add_argument(
        "--rules",
        type=str,
        default="2:3:1,3:5:1,3:7:1,5:7:1",
        help="Comma-separated triples divisor:multiplier:increment",
    )
    p.add_argument("--out", type=str, default="analysis/results/generalized_rule_scan.csv")
    return p.parse_args()


def parse_rules(raw: str) -> list[tuple[int, int, int]]:
    rules: list[tuple[int, int, int]] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        d, m, c = part.split(":")
        rules.append((int(d), int(m), int(c)))
    if not rules:
        raise ValueError("No rules parsed")
    return rules


def run_single_rule(
    limit: int,
    max_steps: int,
    stop_at: int,
    divisor: int,
    multiplier: int,
    increment: int,
) -> dict[str, object]:
    terminated = 0
    cycle_hits = 0
    unresolved = 0
    step_counts: list[int] = []
    peaks: list[int] = []

    for start in range(1, limit + 1):
        n = start
        seen: dict[int, int] = {n: 0}
        peak = n
        reached = False
        cycle_detected = False

        for step in range(1, max_steps + 1):
            n = generalized_next(
                n,
                divisor=divisor,
                nondiv_multiplier=multiplier,
                nondiv_increment=increment,
            )
            if n > peak:
                peak = n

            if n == stop_at:
                terminated += 1
                step_counts.append(step)
                peaks.append(peak)
                reached = True
                break

            if n in seen:
                cycle_hits += 1
                cycle_detected = True
                break
            seen[n] = step

        if not reached and not cycle_detected:
            unresolved += 1

    terminated_frac = terminated / float(limit)
    cycle_frac = cycle_hits / float(limit)
    unresolved_frac = unresolved / float(limit)
    median_steps = int(statistics.median(step_counts)) if step_counts else -1
    median_peak = int(statistics.median(peaks)) if peaks else -1
    max_peak = max(peaks) if peaks else -1

    return {
        "divisor": divisor,
        "multiplier": multiplier,
        "increment": increment,
        "terminated": terminated,
        "terminated_frac": terminated_frac,
        "cycle_hits": cycle_hits,
        "cycle_frac": cycle_frac,
        "unresolved": unresolved,
        "unresolved_frac": unresolved_frac,
        "median_steps_if_terminated": median_steps,
        "median_peak_if_terminated": median_peak,
        "max_peak_if_terminated": max_peak,
    }


def main() -> None:
    args = parse_args()
    rules = parse_rules(args.rules)

    rows: list[dict[str, object]] = []
    for divisor, multiplier, increment in rules:
        row = run_single_rule(
            limit=args.limit,
            max_steps=args.max_steps,
            stop_at=args.stop_at,
            divisor=divisor,
            multiplier=multiplier,
            increment=increment,
        )
        rows.append(row)
        print(
            f"rule d={divisor}, m={multiplier}, c={increment} | "
            f"terminated={row['terminated_frac']:.3f}, cycle={row['cycle_frac']:.3f}, "
            f"unresolved={row['unresolved_frac']:.3f}"
        )

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "divisor",
        "multiplier",
        "increment",
        "terminated",
        "terminated_frac",
        "cycle_hits",
        "cycle_frac",
        "unresolved",
        "unresolved_frac",
        "median_steps_if_terminated",
        "median_peak_if_terminated",
        "max_peak_if_terminated",
    ]
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
