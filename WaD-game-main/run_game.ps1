param(
    [switch]$NoPause
)

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Move to project root (where this script is located)
$ProjectRoot = $ScriptDir

# Change to project root directory
Set-Location -LiteralPath $ProjectRoot

$exitCode = 0
try {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -m game
        $exitCode = $LASTEXITCODE
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        & python -m game
        $exitCode = $LASTEXITCODE
    } else {
        Write-Host "Python not found. Please install Python 3.8+ and ensure it's in PATH." -ForegroundColor Red
        $exitCode = 1
    }
} catch {
    Write-Host "`nFailed to start. Ensure Python is installed and in PATH." -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    $exitCode = 1
}

if ($exitCode -ne 0) {
    Write-Host "Try running from terminal: py -m game" -ForegroundColor Yellow
    Write-Host "Project root: $ProjectRoot" -ForegroundColor Gray
}

if (-not $NoPause) { 
    Read-Host "Press Enter to exit" 
}
exit $exitCode


