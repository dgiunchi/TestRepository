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
- `agents/review/` - external-review style roles (Gemini and Jules) for QA on code, paper, and citations.

## How to use Codex skills
- Skills live in `.agents/skills/<name>/SKILL.md`.
- Prefer invoking a skill explicitly when you're doing role-specific work (LaTeX, literature, stats, viz, orchestration).

## Mandatory reviewer loop
- Every writer task must include reviewer QA before it is considered done.
- Required flow for each task:
  1. Writer agent drafts or implements changes.
  2. Reviewer agent performs an explicit review pass.
  3. Writer addresses findings (or documents why not).
  4. Final output includes a short review status note.
- Reviewer routing:
  - Code/experiments/scripts: use `agents/review/gemini` (or `gemini-reviewer` skill).
  - Paper/docs/citations/editorial quality: use `agents/review/jules` (or `jules-reviewer` skill).
- Minimum acceptance for completion:
  - No unaddressed critical/high-severity findings.
  - Reproducibility checks documented for code changes.
  - Citation and claim checks documented for paper/literature changes.

## Bibliography preflight gate
- Any task touching bibliography or related work must run:
  - `.\.venv\Scripts\python.exe scripts/preflight_related_work.py --bib paper/refs.bib --run-external-checks`
- A writer task is not complete unless this gate returns exit code `0`.
- The resulting report artifact is:
  - `analysis/results/literature_sync_report.json`
- Process details: `docs/agentic/PAPER_PREFLIGHT_GATE.md`

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

