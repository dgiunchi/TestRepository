param()

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$envFile = Join-Path $scriptDir ".env"

if (-not (Test-Path $envFile)) {
  Write-Error "Missing $envFile. Copy mcp/.env-default to mcp/.env and set GITHUB_TOKEN."
}

$tokenLine = Get-Content $envFile |
  Where-Object { $_ -match '^\s*GITHUB_TOKEN\s*=' } |
  Select-Object -First 1

if (-not $tokenLine) {
  Write-Error "GITHUB_TOKEN not found in $envFile."
}

$token = ($tokenLine -split "=", 2)[1].Trim()
if (-not $token) {
  Write-Error "GITHUB_TOKEN is empty in $envFile."
}

& npx -y @modelcontextprotocol/server-github --token $token
