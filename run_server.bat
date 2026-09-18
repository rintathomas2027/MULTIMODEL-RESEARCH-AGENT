@echo off
setlocal
title ScholarPulse AI Studio - Server Launcher

cd /d "%~dp0"

echo ======================================================================
echo   ScholarPulse AI Studio - Server Launcher
echo ======================================================================

set "PYTHON_EXE=venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo.
echo Checking database schema...
%PYTHON_EXE% manage.py migrate

echo.
echo ======================================================================
echo   Starting ScholarPulse AI Studio at http://127.0.0.1:8000/
echo   Press Ctrl+C in this window to stop the server.
echo ======================================================================
echo.

rem Launch browser automatically after 2 seconds
start "" /b cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:8000/"

%PYTHON_EXE% manage.py runserver 127.0.0.1:8000
set "EXIT_CODE=%ERRORLEVEL%"

echo.
echo Server stopped with exit code %EXIT_CODE%.
pause
exit /b %EXIT_CODE%
