#!/usr/bin/env python3
"""Build residue-class transition graph data for Collatz-like rules.

Examples:
  python scripts/exp_residue_transition_graph.py --limit 50000 --modulus 32
  python scripts/exp_residue_transition_graph.py --divisor 3 --nondiv-multiplier 5 --limit 20000 --modulus 27
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from collatz.experiments import residue_transition_matrix  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=20000)
    p.add_argument("--modulus", type=int, default=32)
    p.add_argument("--max-steps", type=int, default=500)
    p.add_argument("--stop-at", type=int, default=1)
    p.add_argument("--divisor", type=int, default=2)
    p.add_argument("--nondiv-multiplier", type=int, default=3)
    p.add_argument("--nondiv-increment", type=int, default=1)
    p.add_argument(
        "--out-csv",
        type=str,
        default="analysis/results/residue_transition_edges.csv",
    )
    p.add_argument(
        "--out-fig",
        type=str,
        default="analysis/results/residue_transition_heatmap.png",
    )
    return p.parse_args()


def write_edges_csv(matrix: np.ndarray, out_csv: Path) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    row_sums = matrix.sum(axis=1)
    with out_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["from_residue", "to_residue", "count", "prob_given_from"])
        for i in range(matrix.shape[0]):
            if row_sums[i] == 0:
                continue
            for j in range(matrix.shape[1]):
                c = int(matrix[i, j])
                if c == 0:
                    continue
                prob = c / float(row_sums[i])
                writer.writerow([i, j, c, f"{prob:.8f}"])


def save_heatmap(matrix: np.ndarray, out_fig: Path, title: str) -> None:
    out_fig.parent.mkdir(parents=True, exist_ok=True)
    row_sums = matrix.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        row_norm = np.divide(matrix, row_sums, out=np.zeros_like(matrix, dtype=float), where=row_sums > 0)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax0 = axes[0]
    im0 = ax0.imshow(np.log1p(matrix), origin="lower", cmap="magma", interpolation="nearest")
    ax0.set_title("log(1 + count)")
    ax0.set_xlabel("to residue")
    ax0.set_ylabel("from residue")
    fig.colorbar(im0, ax=ax0, fraction=0.046, pad=0.04)

    ax1 = axes[1]
    im1 = ax1.imshow(row_norm, origin="lower", cmap="viridis", interpolation="nearest", vmin=0.0, vmax=1.0)
    ax1.set_title("row-normalized transition prob")
    ax1.set_xlabel("to residue")
    ax1.set_ylabel("from residue")
    fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(out_fig, dpi=180)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    result = residue_transition_matrix(
        limit=args.limit,
        modulus=args.modulus,
        max_steps=args.max_steps,
        divisor=args.divisor,
        nondiv_multiplier=args.nondiv_multiplier,
        nondiv_increment=args.nondiv_increment,
        stop_at=args.stop_at,
    )
    matrix = result["matrix"]

    out_csv = ROOT / args.out_csv
    out_fig = ROOT / args.out_fig
    write_edges_csv(matrix, out_csv)

    title = (
        f"Residue transitions (mod {args.modulus}) | "
        f"rule: n%{args.divisor}==0 ? n/{args.divisor} : "
        f"{args.nondiv_multiplier}n+{args.nondiv_increment}"
    )
    save_heatmap(matrix, out_fig, title)

    total_edges = int(result["total_edges"])
    density = float((matrix > 0).sum()) / float(matrix.size)
    print(f"Wrote {out_csv}")
    print(f"Wrote {out_fig}")
    print(
        f"terminated={result['terminated']}, unresolved={result['unresolved']}, "
        f"edges={total_edges}, matrix_density={density:.4f}"
    )


if __name__ == "__main__":
    main()
