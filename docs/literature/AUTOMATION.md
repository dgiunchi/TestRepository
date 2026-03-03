# Literature Automation (BibTeX -> Zotero -> PDFs -> Knowledge Notes)

This repo includes `scripts/lit_sync_pipeline.py` to automate literature ingestion.

## What it does
- Parses `paper/refs.bib`
- Validates each entry against DOI/arXiv identifiers
- Optionally syncs items into an existing Zotero group library
- Optionally downloads available PDFs
- Writes knowledge-note stubs per citation key
- Emits a reproducibility report JSON

## Run

```powershell
.\.venv\Scripts\python.exe scripts/lit_sync_pipeline.py `
  --bib paper/refs.bib `
  --report-json analysis/results/literature_sync_report.json `
  --download-pdfs `
  --run-external-checks `
  --strict
```

Preflight wrapper (recommended for writer agents):

```powershell
.\.venv\Scripts\python.exe scripts/preflight_related_work.py --bib paper/refs.bib --run-external-checks
```

Default knowledge folder:
- `docs/literature/skill_knowledge/`
  - `pdfs/`
  - `notes/`

## Zotero sync

Set your API key first:

```powershell
$env:ZOTERO_API_KEY="your_zotero_key"
```

Then run:

```powershell
.\.venv\Scripts\python.exe scripts/lit_sync_pipeline.py `
  --sync-zotero `
  --zotero-user-id "<your_user_id>" `
  --zotero-group-id "<existing_group_id>"
```

Notes:
- The script writes to an existing group library.
- If you prefer name lookup, use `--zotero-group-name` with `--zotero-user-id`.
- If a group name is not found, create it once in Zotero UI and rerun.
- External checker defaults to `npx -y bibtex-tidy`. Override with:
  `--external-checker-bin` and `--external-checker-package`.
