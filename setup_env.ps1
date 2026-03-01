param(
    [string]$VenvDir = ".venv"
)

$ErrorActionPreference = "Stop"

Write-Host "Creating virtual environment in '$VenvDir'..."
python -m venv $VenvDir

$pythonExe = Join-Path $VenvDir "Scripts\python.exe"

Write-Host "Upgrading pip..."
& $pythonExe -m pip install --upgrade pip

Write-Host "Installing requirements from requirements.txt..."
& $pythonExe -m pip install -r requirements.txt

Write-Host ""
Write-Host "Environment ready."
Write-Host "Activate with:"
Write-Host "  $VenvDir\Scripts\Activate.ps1"
