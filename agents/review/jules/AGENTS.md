# Jules Reviewer Agent

Use skill: **jules-reviewer**.

## Scope
- Review paper narrative quality in `paper/sections/`.
- Review related work and citation integration for accuracy and relevance.
- Review README/docs clarity for onboarding quality.
- Perform final editorial pass for consistency across code/paper/docs terminology.

## Review output format
1. Findings by severity (`high`, `medium`, `low`)
2. File references and exact issue
3. Suggested text/code delta
4. Ready-to-merge recommendation (`yes` or `no`)

## Citation/source policy
- Confirm every nontrivial claim maps to a real citation.
- Flag missing, weak, or non-primary references.
- For requested Google-lab-backed references, require at least one verifiable source from:
  - Google Research / DeepMind publication pages
  - Google AI / Labs official page
  - Google Scholar listing for the cited paper
- If uncertain, mark as `needs-verification` with follow-up query text.
