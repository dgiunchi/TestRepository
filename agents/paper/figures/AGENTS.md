# Paper Figures Agent

Use skills: **viz-engineer**, **stats-engineer**.

## Scope
- Turn statistical outputs into publication-quality figures for `paper/figures/`.
- Reuse CSV outputs from `analysis/results/` and reproducible scripts in `scripts/plot_*.py`.
- Keep figure style/labels consistent with paper notation.

## Working agreement with stats agent
- Input contract: stats agent writes tidy CSVs with documented columns and parameters.
- Output contract: this agent writes deterministic plot scripts and exports figure files with stable names.
- Every figure used in the paper must be reproducible from a script command.
