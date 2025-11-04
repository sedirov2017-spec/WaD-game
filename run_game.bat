@echo off
setlocal

:: Move to the project root (parent of this script's folder)
pushd %~dp0..

:: Prefer Windows launcher
where py >nul 2>nul
if %errorlevel%==0 (
  py -m game
) else (
  python -m game
)

if %errorlevel% neq 0 (
  echo.
  echo Failed to start. Ensure Python is installed and available in PATH.
  echo Try running from terminal: py -m game
  pause
)

popd
endlocal


