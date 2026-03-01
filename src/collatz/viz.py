"""Visualization helpers.

Implementation lives here; runnable scripts belong in `scripts/`.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_complex_escape(result: dict[str, np.ndarray], out_path: str | Path) -> None:
    """Render a two-panel complex-space diagnostic plot."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    xs = result["xs"]
    ys = result["ys"]
    escape_steps = result["escape_steps"]
    escaped_mask = result["escaped_mask"]
    min_dist_to_one = result["min_dist_to_one"]

    extent = (float(xs[0]), float(xs[-1]), float(ys[0]), float(ys[-1]))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax0 = axes[0]
    im0 = ax0.imshow(
        escape_steps,
        origin="lower",
        extent=extent,
        cmap="magma",
        aspect="auto",
        interpolation="nearest",
    )
    ax0.set_title("Escape steps")
    ax0.set_xlabel("Re(z)")
    ax0.set_ylabel("Im(z)")
    c0 = fig.colorbar(im0, ax=ax0)
    c0.set_label("steps")

    ax1 = axes[1]
    stable_proxy = np.log10(np.maximum(min_dist_to_one, 1e-12))
    stable_proxy = np.clip(stable_proxy, -12, 4)
    im1 = ax1.imshow(
        stable_proxy,
        origin="lower",
        extent=extent,
        cmap="viridis",
        aspect="auto",
        interpolation="nearest",
    )
    ax1.contour(
        escaped_mask.astype(float),
        levels=[0.5],
        origin="lower",
        extent=extent,
        colors="white",
        linewidths=0.6,
        alpha=0.7,
    )
    ax1.set_title("log10(min |z_k - 1|)")
    ax1.set_xlabel("Re(z)")
    ax1.set_ylabel("Im(z)")
    c1 = fig.colorbar(im1, ax=ax1)
    c1.set_label("log10 distance")

    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)
