@echo off
setlocal

set VERSION=%1
if "%VERSION%"=="" set VERSION=1.6.0

if not exist "%USERPROFILE%\iopaint-models" mkdir "%USERPROFILE%\iopaint-models"

docker run --rm -it ^
  --gpus all ^
  -p 8080:8080 ^
  -v "%USERPROFILE%\iopaint-models:/root/.cache" ^
  iopaint:gpu-%VERSION% ^
  iopaint start --host 0.0.0.0 --model lama --device cuda --no-half --port 8080

pause
