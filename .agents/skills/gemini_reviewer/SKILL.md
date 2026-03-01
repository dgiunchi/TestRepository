---
name: gemini-reviewer
description: Perform strict technical review for code, experiments, and paper-methods consistency. Use when a change needs bug/risk detection, reproducibility checks, and source-verification of technical claims, including Google-lab-backed references.
---

# Gemini Reviewer Skill

## Where to review
- `src/`, `scripts/`, `tests/`
- `analysis/`
- `paper/sections/methods.tex`
- `paper/sections/experiments.tex`
- `paper/refs.bib`

## Workflow
1. Identify behavioral regressions and correctness risks first.
2. Check reproducibility: script entrypoints, parameters, and outputs.
3. Check method/experiment consistency between code and paper text.
4. Validate references behind technical claims.

## Output contract
- List findings by severity: `high`, `medium`, `low`.
- Include file path and exact issue.
- Provide concrete fix guidance.
- State what was not verified.

## Google-lab verification rule
For claims marked as requiring Google-lab backing, verify using at least one:
- Google Research publications
- Google DeepMind publications
- Google AI or Google Labs official pages
- Google Scholar metadata page

If not verified, mark `unverified` and request a replacement source.
