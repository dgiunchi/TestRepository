# Review Agents

This folder defines external-review style roles focused on quality gates before merge:
- code quality and correctness review
- paper quality and argument clarity review
- bibliography and citation validity review

Sub-roles:
- `gemini/` - technical and methodological reviewer
- `jules/` - writing, structure, and citation reviewer

Escalate major concerns to `agents/orchestrator/INBOX.md` with:
- severity (`high`, `medium`, `low`)
- affected files
- required action
