# MCP (optional)

This repo is set up to work well with **Codex + GitHub** out of the box.

If you use additional MCP servers (e.g., filesystem access, GitHub actions, memory), keep their configuration here.

- `mcp.example.json` is a *template* you can copy and adjust.
- `mcp.example.json` now includes a practical starter set:
  - `filesystem` for repo-local file operations
  - `github` for issue/PR workflows (reads token from `mcp/.env`)
  - `memory` for persistent notes/context

## Quick start
1. Ensure Node.js is installed (for `npx`).
2. Copy `mcp/.env-default` to `mcp/.env`.
3. Set `GITHUB_TOKEN` in `mcp/.env`.
4. Copy `mcp/mcp.example.json` into your MCP client config location.
5. Restart your MCP client and confirm servers appear in the list.

## Where to create `GITHUB_TOKEN`
1. Go to GitHub -> `Settings` -> `Developer settings` -> `Personal access tokens`.
2. Create a token (fine-grained recommended).
3. Grant minimum repo permissions you need (for example: repository contents, pull requests, issues).
4. Paste it into `mcp/.env` as:

```env
GITHUB_TOKEN=ghp_or_github_pat_value
```

Only the `github` MCP server uses this token. `filesystem` and `memory` do not need it.

> Note: exact MCP configuration depends on the client you use (Codex CLI, editor integration, etc.). Treat this folder as the place to document and version the configuration for your workflow.
