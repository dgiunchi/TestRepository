# Gemini Reviewer Agent

Use skill: **gemini-reviewer**.

## Scope
- Review Python code in `src/`, `scripts/`, and root utilities.
- Review experiment setup for reproducibility and statistical hygiene.
- Review paper methods/experiments sections for technical consistency.
- Validate that cited technical claims are traceable to real sources.

## Review output format
1. Findings by severity (`high`, `medium`, `low`)
2. File references and exact issue
3. Suggested fix
4. Validation status (tests/build/checks run or not run)

## Citation/source policy
- Prefer primary sources (official docs, papers, publisher pages).
- For "Google lab" requirements, verify against at least one:
  - Google Research publications
  - Google DeepMind publications
  - Google AI / Google Labs official pages
  - Google Scholar metadata page for the cited work
- If source cannot be verified, mark as `unverified` and request replacement.
