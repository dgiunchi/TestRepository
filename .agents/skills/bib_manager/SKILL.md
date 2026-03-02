---
name: bib-manager
description: Maintain the BibTeX database and citations for the paper. Ensure keys are consistent, fields are complete, and citations appear where needed.
metadata:
  short-description: Maintain refs and citation keys
---

# Bibliography Manager Skill

## Where to work
- `paper/refs.bib`
- `paper/sections/related_work.tex`

## Rules
- Use consistent keys: `AuthorYYYYShortTitle`.
- Prefer DOI and URL fields when available.
- Avoid duplicate entries; merge instead.

## Deliverables
- Clean `refs.bib`
- No missing citation keys in LaTeX build (or explicitly marked TODO)
