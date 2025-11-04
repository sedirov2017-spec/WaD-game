@echo off
setlocal enabledelayedexpansion

:: Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

:: Move to the project root (where this script is located)
pushd "%SCRIPT_DIR%"

:: Store the current directory
set "PROJECT_ROOT=%CD%"
set "EXIT_CODE=0"

:: Prefer Windows launcher
where py >nul 2>nul
if %errorlevel%==0 (
  py -m game
  set "EXIT_CODE=!errorlevel!"
) else (
  python -m game
  set "EXIT_CODE=!errorlevel!"
)

if !EXIT_CODE! neq 0 (
  echo.
  echo Failed to start. Ensure Python is installed and available in PATH.
  echo Try running from terminal: py -m game
  echo Project root: %PROJECT_ROOT%
  pause
)

popd
endlocal & set "EXIT_CODE=%EXIT_CODE%"
exit /b %EXIT_CODE%


