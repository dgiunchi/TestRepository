---
name: jules-reviewer
description: Perform editorial and literature-quality review for paper/docs plus citation integrity checks. Use when validating writing clarity, argument structure, related-work quality, and reference authenticity including Google-lab-backed sources.
---

# Jules Reviewer Skill

## Where to review
- `paper/sections/`
- `paper/main.tex`
- `paper/refs.bib`
- `README.md`, `docs/`

## Workflow
1. Review structure and readability of scientific narrative.
2. Check that claims are supported and properly cited.
3. Validate related-work positioning and novelty statements.
4. Ensure terminology consistency across paper, docs, and code.

## Output contract
- Findings grouped by severity: `high`, `medium`, `low`.
- File path and exact problematic text/claim.
- Suggested rewrite or citation fix.
- Final recommendation: `ready` or `not-ready`.

## Google-lab verification rule
For references that must exist from Google labs/research ecosystem, verify using at least one:
- Google Research or DeepMind publication page
- Google AI/Labs official page
- Google Scholar listing

If verification fails, mark `needs-verification` and propose replacement citation targets.
