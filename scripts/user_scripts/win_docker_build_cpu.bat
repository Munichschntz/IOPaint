@echo off
setlocal

set ROOT=%~dp0\..\..
cd /d "%ROOT%"

set VERSION=%1
if "%VERSION%"=="" set VERSION=1.6.0

docker build -f docker\CPUDockerfile -t iopaint:cpu-%VERSION% --build-arg version=%VERSION% .
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo Built image iopaint:cpu-%VERSION%
pause
