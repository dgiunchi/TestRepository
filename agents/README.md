# Agents

These folders are *workspaces* for different roles. When you run **Codex CLI** from within a folder, Codex will load:
- root `AGENTS.md`
- this folder's `AGENTS.md`

Use this to give each role a clear scope and avoid stepping on each other.

Suggested usage:
- `codex --cd agents/paper/latex "..."`
- `codex --cd agents/paper/figures "Generate/update figures from analysis/results for paper/figures."`
- `codex --cd agents/code/stats "..."`
- `codex --cd agents/review/gemini "..."`
- `codex --cd agents/review/jules "..."`

Each agent folder can keep:
- `INBOX.md` - tasks assigned to that agent
- `NOTES.md` - scratchpad and decisions

