---
name: viz-engineer
description: Implement visualizations (static + animated) from specs. Keep APIs stable, prefer Matplotlib for reproducibility, and export figures for the paper.
---

# Visualization Engineer Skill

## Where to work
- `src/collatz/viz.py`
- `scripts/plot_*.py`
- `paper/figures/` (exported SVG/PDF/PNG)

## Rules
- Every script should be runnable from repo root.
- Save figures with a predictable name and include a short caption in `paper/figures/README.md`.
- Avoid interactive-only dependencies unless requested.
