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

3) Explore a complex-plane extension map:

```bash
python scripts/exp_complex_escape_map.py --width 900 --height 900 --steps 160 --out analysis/results/complex_escape_map.png
```

4) Build residue transition graph data (classic or generalized rule):

```bash
python scripts/exp_residue_transition_graph.py --limit 50000 --modulus 32
python scripts/exp_residue_transition_graph.py --divisor 3 --nondiv-multiplier 5 --limit 20000 --modulus 27
```

5) Scan generalized rule families:

```bash
python scripts/exp_generalized_rule_scan.py --limit 5000 --rules "2:3:1,3:5:1,3:7:1,5:7:1"
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
- Review: Gemini + Jules reviewer roles for code QA, paper QA, and citation/source verification

Example (run Codex in a role folder):

```bash
codex --cd agents/paper/latex "Update the paper outline and ensure it compiles."
```

Reviewer examples:

```bash
codex --cd agents/review/gemini "Review the new experiment script and flag correctness risks."
codex --cd agents/review/jules "Review Introduction + Related Work and verify citations are real and relevant."
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

---

## MCP setup (optional)

This repo includes `mcp/mcp.json` and `mcp/mcp.example.json` with starter servers:
- `filesystem`
- `github`
- `memory`

If you cannot set system environment variables, use a local file:

1. Copy `mcp/.env-default` to `mcp/.env`
2. Put your token in `mcp/.env`:

```env
GITHUB_TOKEN=ghp_or_github_pat_value
```

Only the `github` MCP server needs this token.

