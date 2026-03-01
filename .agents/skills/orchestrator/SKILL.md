---
name: collatz-orchestrator
description: Plan and coordinate multi-agent work for the Collatz research repo. Maintain ROADMAP.md, keep tasks small, and route work to the right agent folders without doing heavy implementation yourself.
---

# Collatz Orchestrator Skill

## When to use
Use this skill when the user asks to:
- Plan the research/paper roadmap
- Break a big goal into agent-sized tasks
- Set up GitHub issues/PR plan, labels, milestones
- Decide where a change should live in the repo

## What to do
1. **Clarify the deliverable** (paper section, experiment, visualization, code refactor).
2. **Create/refresh `ROADMAP.md`** with:
   - near-term milestones (1-2 weeks)
   - current hypotheses/ideas queue
   - experiments backlog
   - paper TODO by section
3. **Assign work to folders**:
   - `paper/` for LaTeX + figures
   - `src/` + `analysis/` for code/experiments
   - `docs/` for design notes
4. **Define acceptance criteria** for each task (tests, plots, PDF build success, reproducible script).
5. Prefer **small PRs**: one concept per PR.

## What NOT to do
- Don't implement large code changes unless explicitly asked.
- Don't write/modify many paper sections at once; delegate.

## Suggested outputs
- A task list with owners (agent folders) and files to touch
- A short checklist for each task

