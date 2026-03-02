# MCP integration notes

Potential MCP servers that fit this repo:

## Literature + references
- Search (arXiv / Crossref) -> populate `docs/literature/` and `paper/refs.bib`
- Zotero (or other library manager) -> keep bib entries consistent

## Compute + data
- A local execution MCP for running long experiments, generating CSVs, and exporting figures

## GitHub workflow
- Issue/PR automation: create issues from `ROADMAP.md`, label by agent role, and request reviews

## Starter config in this repo
- Use `mcp/mcp.example.json` as a base config.
- Included starter servers:
  - `filesystem` (scoped to this repository path)
  - `github` (token read from `mcp/.env`)
  - `memory`
- Copy `mcp/.env-default` to `mcp/.env`, then set `GITHUB_TOKEN`.
- Only the `github` MCP server needs this token.

**Recommendation:** keep any secrets in env vars and never commit them.
