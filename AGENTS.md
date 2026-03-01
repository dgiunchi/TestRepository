# Collatz Lab - Agent Instructions (Codex)

## Mission
This repository is a research workspace for computational and expository study of the **Collatz (3x+1) conjecture**.

We maintain:
- Reproducible **code** for experiments and visualizations (`src/`, `scripts/`, `analysis/`).
- A publishable **paper** (`paper/`) and supporting literature notes (`docs/`).
- A multi-agent workflow (folders under `agents/` + Codex **skills** in `.agents/skills/`).

## Golden rules
1. **Reproducibility first**: every result must be regenerable from a script with parameters recorded.
2. **One concept per change**: keep PRs focused.
3. **Conservative claims**: do not claim proofs; label heuristics/empirics clearly.
4. **Paper <-> code traceability**: figures and tables in the paper should be produced by scripts.

## Repo map (high level)
- `paper/` - LaTeX paper (PDF) + HTML companion using PrismJS + MathJax.
- `src/collatz/` - core library (sequence generation, stats utilities, viz helpers).
- `scripts/` - runnable entrypoints to generate datasets/figures.
- `analysis/` - notebooks, experiment logs, and small results.
- `docs/` - literature map, idea queue, visualization specs.
- `agents/` - role folders with local instructions and scratchpads.

## How to use Codex skills
- Skills live in `.agents/skills/<name>/SKILL.md`.
- Prefer invoking a skill explicitly when you're doing role-specific work (LaTeX, literature, stats, viz, orchestration).

## Default commands
### Python
- Create venv: `python -m venv .venv`
- Install: `pip install -r requirements.txt`

### Paper
- Build PDF (from `paper/`): `latexmk -pdf -interaction=nonstopmode -output-directory=build main.tex`

## Where to put things
- New hypotheses/ideas: `docs/ideas/`
- Literature notes: `docs/literature/`
- Visualization specs: `docs/visualizations/`
- Scripts that generate paper figures: `scripts/plot_*.py` and output to `paper/figures/`
- Paper text: `paper/sections/*.tex`

## Safety / scope
- Do not add large external datasets to git.
- Keep generated artifacts out of version control unless small and essential.

