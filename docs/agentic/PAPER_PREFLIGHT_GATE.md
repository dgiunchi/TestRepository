# Paper Preflight Gate (Reusable Agent Workflow)

## Scope
Run this before finalizing any edits to:
- `paper/refs.bib`
- `paper/sections/related_work.tex`
- any section that adds/changes citation keys

## Required command

```powershell
.\.venv\Scripts\python.exe scripts/preflight_related_work.py --bib paper/refs.bib --run-external-checks
```

## Pass/fail
- Pass: exit code `0`
- Fail: non-zero exit; do not finalize writing task

## Output artifact
- `analysis/results/literature_sync_report.json`

## Reviewer handoff
After gate passes:
- Code/bib tooling review: `gemini-reviewer`
- Writing/citation quality review: `jules-reviewer`
