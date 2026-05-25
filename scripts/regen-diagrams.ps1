# Wrapper that installs npm deps (if needed) and runs the diagram regenerator.
# Run from the repo root: pwsh -File scripts/regen-diagrams.ps1

$ErrorActionPreference = "Stop"
$scriptDir = $PSScriptRoot

Push-Location $scriptDir
try {
    if (-not (Test-Path "$scriptDir\node_modules\puppeteer-core")) {
        Write-Host "Installing npm dependencies (puppeteer-core)..." -ForegroundColor Cyan
        npm install --no-audit --no-fund
        if ($LASTEXITCODE -ne 0) { throw "npm install failed" }
    }

    Write-Host "Regenerating diagrams..." -ForegroundColor Cyan
    node "$scriptDir\regen-diagrams.mjs"
    if ($LASTEXITCODE -ne 0) { throw "regen-diagrams.mjs exited with code $LASTEXITCODE" }
}
finally {
    Pop-Location
}

Write-Host "`nDone. PNGs written to docs/diagrams/" -ForegroundColor Green
