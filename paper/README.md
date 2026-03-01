# Paper

This folder contains:
- `main.tex` - the LaTeX manuscript (builds to PDF)
- `sections/` - section files
- `figures/` - exported figures for the PDF
- `tables/` - generated tables (if any)
- `web/` - an HTML companion page for quick sharing, using **PrismJS** + **MathJax**

## Build the PDF
From this folder:

```bash
latexmk -pdf -interaction=nonstopmode -output-directory=build main.tex
```

If you want syntax-highlighted code in PDF via `minted`, you may need:
- `-shell-escape`
- Pygments installed

A fallback to `listings` is enabled automatically if `minted` is missing.

