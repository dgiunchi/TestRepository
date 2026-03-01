#!/usr/bin/env python3
"""Create baseline plots from the range dataset.

Usage:
  python scripts/plot_baseline_range.py --csv analysis/results/baseline_100k.csv --outdir paper/figures

If --csv is omitted, the script computes data on the fly (slower).
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from collatz.core import collatz_sequence  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=5000, help="Used if --csv is not provided")
    p.add_argument("--max-steps", type=int, default=10000)
    p.add_argument("--csv", type=str, default="")
    p.add_argument("--outdir", type=str, default="paper/figures")
    return p.parse_args()


def load_or_compute(args: argparse.Namespace) -> tuple[list[int], list[int], list[int]]:
    if args.csv:
        starts: list[int] = []
        stops: list[int] = []
        peaks: list[int] = []
        with (ROOT / args.csv).open("r", newline="") as f:
            r = csv.DictReader(f)
            for row in r:
                starts.append(int(row["start"]))
                stops.append(int(row["stopping_time"]))
                peaks.append(int(row["peak"]))
        return starts, stops, peaks

    starts = list(range(1, args.limit + 1))
    stops: list[int] = []
    peaks: list[int] = []
    for n in starts:
        seq = collatz_sequence(n, max_steps=args.max_steps)
        if seq[-1] != 1:
            # Skip unresolved values.
            continue
        stops.append(len(seq) - 1)
        peaks.append(max(seq))
    # Note: starts list may be longer than stops/peaks if there are skips; keep aligned.
    starts = starts[: len(stops)]
    return starts, stops, peaks


def savefig(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def main() -> None:
    args = parse_args()
    outdir = ROOT / args.outdir

    starts, stops, peaks = load_or_compute(args)

    # 1) stopping time landscape
    plt.figure()
    plt.plot(starts, stops, linewidth=1)
    plt.xlabel("start n")
    plt.ylabel("stopping time σ(n)")
    plt.title("Stopping time by start value")
    savefig(outdir / "baseline_stopping_time.png")

    # 2) peak landscape
    plt.figure()
    plt.plot(starts, peaks, linewidth=1)
    plt.xlabel("start n")
    plt.ylabel("peak π(n)")
    plt.title("Peak by start value")
    savefig(outdir / "baseline_peak.png")

    # 3) joint scatter
    plt.figure()
    plt.scatter(stops, peaks, s=6, alpha=0.6)
    plt.xlabel("stopping time σ(n)")
    plt.ylabel("peak π(n)")
    plt.title("Stopping time vs peak")
    savefig(outdir / "baseline_stop_vs_peak.png")

    print(f"Wrote figures to {outdir}")


if __name__ == "__main__":
    main()
