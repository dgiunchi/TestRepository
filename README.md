# Collatz Lab: Visualizing and Experimenting with the 3n+1 Conjecture

This repository is a **research workspace** for the Collatz (3x+1) conjecture.

It combines:
- **Code** for reproducible experiments and visualizations
- A **LaTeX paper** (and a lightweight HTML companion)
- A **multi-agent workflow** designed for Codex CLI + GitHub

> This project is exploratory and does **not** claim a proof of the conjecture.

---

## Quick start (Python)

### 1) Create and activate a virtual environment

**Linux/macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
.\setup_env.ps1
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

Optional (tests/lint):

```bash
pip install -r requirements-dev.txt
```

### 3) Run the interactive tools

CLI explorer:

```bash
python collatz_explorer.py --mode both --start 27 --limit 500
```

Animated UI:

```bash
python collatz_animated_ui.py
```

---

## Baseline experiment pipeline

1) Generate a dataset:

```bash
python scripts/exp_baseline_dataset.py --limit 100000 --out analysis/results/baseline_100k.csv
```

2) Generate paper-ready figures:

```bash
python scripts/plot_baseline_range.py --csv analysis/results/baseline_100k.csv --outdir paper/figures
```

---

## Paper

The manuscript lives in `paper/`.

Build the PDF:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -output-directory=build main.tex
```

There is also a lightweight HTML companion at `paper/web/index.html` that uses **MathJax** + **PrismJS** for quick sharing.

---

## Multi-agent organization (Codex)

### Instruction files
- Root `AGENTS.md` defines repo-wide rules.
- Each folder under `agents/` may include its own `AGENTS.md` to scope a role.

### Skills
Codex skills live in `.agents/skills/*/SKILL.md`.

Suggested roles:
- Orchestrator: planning + task decomposition
- Paper: LaTeX + intro + related work + references
- Research: new ideas + new visualization concepts
- Code: stats analysis + visualization implementation + experiment scripts

Example (run Codex in a role folder):

```bash
codex --cd agents/paper/latex "Update the paper outline and ensure it compiles."
```

---

## Repository layout

- `src/collatz/` - canonical core library
- `scripts/` - reproducible experiment/plot entrypoints
- `analysis/` - notebooks and small results
- `paper/` - LaTeX manuscript + figures + HTML companion
- `docs/` - literature map, idea queue, visualization specs
- `agents/` - role workspaces for Codex
- `.agents/skills/` - Codex skills

---

## Tests

```bash
pytest
```

