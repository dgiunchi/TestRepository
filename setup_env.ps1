param(
    [string]$VenvDir = ".venv",
    [switch]$Dev
)

$ErrorActionPreference = "Stop"

Write-Host "Creating virtual environment in '$VenvDir'..."
python -m venv $VenvDir

$pythonExe = Join-Path $VenvDir "Scripts\python.exe"

Write-Host "Upgrading pip..."
& $pythonExe -m pip install --upgrade pip

Write-Host "Installing runtime requirements..."
& $pythonExe -m pip install -r requirements.txt

Write-Host "Installing package (editable)..."
& $pythonExe -m pip install -e .

if ($Dev) {
    Write-Host "Installing dev requirements..."
    & $pythonExe -m pip install -r requirements-dev.txt
}

Write-Host ""
Write-Host "Environment ready."
Write-Host "Activate with:"
Write-Host "  $VenvDir\Scripts\Activate.ps1"
