@echo off
setlocal

set ROOT=%~dp0\..\..
cd /d "%ROOT%"

if not exist ".venv\Scripts\activate.bat" (
  echo Missing virtual environment. Run win_native_setup_cpu.bat first.
  pause
  exit /b 1
)

call .venv\Scripts\activate.bat
iopaint start --model lama --device cpu --port 8080 --inbrowser

pause
