#!/usr/bin/env python3
"""Generate a complex-plane Collatz extension escape map.

This script uses an analytic parity proxy:
  p(z) = (1 - cos(pi z)) / 2
and the blended map:
  T(z) = (1 - p(z)) * (z / 2) + p(z) * (3z + 1)

For integer z = n, this matches the classical Collatz rule exactly.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from collatz.experiments import complex_escape_grid  # noqa: E402
from collatz.viz import plot_complex_escape  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute and visualize complex-space dynamics for a Collatz extension."
    )
    parser.add_argument("--re-min", type=float, default=-3.0)
    parser.add_argument("--re-max", type=float, default=3.0)
    parser.add_argument("--im-min", type=float, default=-3.0)
    parser.add_argument("--im-max", type=float, default=3.0)
    parser.add_argument("--width", type=int, default=700)
    parser.add_argument("--height", type=int, default=700)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--escape-radius", type=float, default=100.0)
    parser.add_argument(
        "--out",
        type=str,
        default="analysis/results/complex_escape_map.png",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = complex_escape_grid(
        re_min=args.re_min,
        re_max=args.re_max,
        im_min=args.im_min,
        im_max=args.im_max,
        width=args.width,
        height=args.height,
        max_steps=args.steps,
        escape_radius=args.escape_radius,
    )
    out = ROOT / args.out
    plot_complex_escape(result, out)

    escaped_fraction = float(result["escaped_mask"].mean())
    print(f"Wrote {out}")
    print(
        f"Grid: {args.width}x{args.height}, steps={args.steps}, escape_fraction={escaped_fraction:.4f}"
    )


if __name__ == "__main__":
    main()
