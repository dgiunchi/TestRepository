---
name: latex-prism
description: Write and maintain the LaTeX paper in paper/. Use clean math, consistent notation, and add code listings suitable for PrismJS (HTML) and PDF (minted/listings). Ensure the paper builds.
---

# LaTeX + Prism Skill

## Scope
- Edit `paper/main.tex` and `paper/sections/*.tex`
- Create figures in `paper/figures/` and include them
- Maintain the HTML companion in `paper/web/` that uses **PrismJS** + **MathJax**

## Build targets
- **PDF**: `latexmk -pdf -interaction=nonstopmode -output-directory=build main.tex`
- **HTML notes**: open `paper/web/index.html` in a browser

## Code listings strategy
- For PDF: prefer `minted` if available; otherwise fall back to `listings`.
- For HTML: add code blocks with `class="language-python"` etc so Prism highlights.

## LaTeX conventions
- Put definitions/lemmas in theorem environments.
- Keep notation in `paper/sections/notation.tex` and reuse.
- Every claim that depends on literature must have a citation placeholder `\cite{...}`.

## Output checklist
- `latexmk` succeeds
- No undefined references remain (or they are explicit TODOs)
- New macros documented in `paper/sections/notation.tex`
