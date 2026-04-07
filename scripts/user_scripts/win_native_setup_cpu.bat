@echo off
setlocal

set ROOT=%~dp0\..\..
cd /d "%ROOT%"

if not exist ".venv" (
  where py >nul 2>nul
  if %errorlevel%==0 (
    py -3 -m venv .venv
  ) else (
    python -m venv .venv
  )
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install torch torchvision
pip install -e .
iopaint install-plugins-packages

echo.
echo Native CPU environment is ready.
echo Start with: scripts\user_scripts\win_native_start_cpu.bat
pause
