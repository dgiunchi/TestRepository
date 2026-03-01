# Codex workflow

## Where instructions live
- Repo-wide: `AGENTS.md`
- Role-specific: `agents/**/AGENTS.md`
- Skills: `.agents/skills/**/SKILL.md`

Codex loads `AGENTS.md` files from the repo root down to your current working directory.

## Suggested loop
1. Orchestrator breaks down a goal into tasks and updates `ROADMAP.md`.
2. Role agents work in parallel:
   - paper drafting in `paper/sections/`
   - literature in `docs/literature/` + `paper/refs.bib`
   - experiments/plots in `src/` + `scripts/`
3. Each task lands as a small PR.

## Examples

### Update the introduction
```bash
codex --cd agents/paper/intro "Draft a tighter introduction in paper/sections/introduction.tex."
```

### Add a new visualization spec
```bash
codex --cd agents/research/visualizations "Propose 2 new plot ideas and write specs in docs/visualizations/."
```

### Implement a plot script
```bash
codex --cd agents/code/viz "Implement the spec 'residue-class heatmap' and add a script under scripts/."
```
