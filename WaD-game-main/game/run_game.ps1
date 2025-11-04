param(
    [switch]$NoPause
)

# Move to project root (parent of this script's directory)
Set-Location (Split-Path $PSScriptRoot -Parent)

$exitCode = 0
try {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -m game
        $exitCode = $LASTEXITCODE
    } else {
        python -m game
        $exitCode = $LASTEXITCODE
    }
} catch {
    Write-Host "`nFailed to start. Ensure Python is installed and in PATH." -ForegroundColor Red
    $exitCode = 1
}

if ($exitCode -ne 0) {
    Write-Host "Try running from terminal: py -m game" -ForegroundColor Yellow
}

if (-not $NoPause) { Read-Host "Press Enter to exit" }
exit $exitCode


