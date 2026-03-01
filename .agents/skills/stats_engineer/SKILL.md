---
name: stats-engineer
description: Implement statistical analyses for Collatz experiments (distributions, tail behavior, regressions, hypothesis checks). Produce clean datasets and plots with reproducible scripts.
---

# Stats Engineer Skill

## Where to work
- `src/collatz/stats.py`
- `analysis/` (notebooks or scripts)
- `analysis/results/` for generated data (keep small; large data should be gitignored)

## Rules
- Provide a deterministic seed where randomness is used.
- Save results with metadata (parameters, commit hash if available).
- Prefer simple, robust stats (quantiles, ECDFs, log-log plots) before fancy modeling.
