# AI_OS Command Center — Startup Script
# Port 8006 | FastAPI + SQLite

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir   = Join-Path $ScriptDir ".venv"
$Python    = Join-Path $VenvDir "Scripts\python.exe"
$Pip       = Join-Path $VenvDir "Scripts\pip.exe"
$FallbackPy = "D:\AI_OS\04_projects\Quantara\.venv\Scripts\python.exe"
$Server    = Join-Path $ScriptDir "server.py"

Write-Host "`n AI_OS Command Center" -ForegroundColor Cyan
Write-Host " ─────────────────────────────" -ForegroundColor DarkGray

# 1. Create venv if needed
if (-not (Test-Path $Python)) {
    Write-Host " [1/3] Creating virtual environment..." -ForegroundColor Yellow
    if (Test-Path $FallbackPy) { & $FallbackPy -m venv $VenvDir }
    else { python -m venv $VenvDir }
    if ($LASTEXITCODE -ne 0) { Write-Host " ERROR: python not found" -ForegroundColor Red; exit 1 }
    Write-Host "       Done." -ForegroundColor Green
} else {
    Write-Host " [1/3] venv ready" -ForegroundColor Green
}

# 2. Install dependencies
Write-Host " [2/3] Installing dependencies..." -ForegroundColor Yellow
& $Pip install -r (Join-Path $ScriptDir "requirements.txt") --quiet 2>&1 | Select-Object -Last 2
Write-Host "       Done." -ForegroundColor Green

# 3. Start server
Write-Host " [3/3] Starting dashboard at http://localhost:8006" -ForegroundColor Yellow
Write-Host "       Press Ctrl+C to stop.`n" -ForegroundColor DarkGray

Set-Location $ScriptDir
& $Python -m uvicorn server:app --host 0.0.0.0 --port 8006 --reload
