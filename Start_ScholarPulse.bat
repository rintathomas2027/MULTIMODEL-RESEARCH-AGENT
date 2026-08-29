@echo off
setlocal
title ScholarPulse AI Studio

rem Always run from the folder that contains this launcher.
cd /d "%~dp0"

echo ==============================================
echo   ScholarPulse AI - Starting Local Server
echo ==============================================

if not exist "venv\Scripts\python.exe" (
    echo.
    echo Python virtual environment was not found.
    echo Expected: %CD%\venv\Scripts\python.exe
    echo.
    pause
    exit /b 1
)

echo Updating database schema...
"venv\Scripts\python.exe" manage.py migrate

echo.
echo Starting server at http://127.0.0.1:8000/
echo Opening browser...
echo Press Ctrl+C to stop the server.
echo ==============================================

rem Open browser in background after 2 seconds
start "" /b cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:8000/"

"venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
set "SERVER_EXIT_CODE=%ERRORLEVEL%"

echo.
echo Server stopped with exit code %SERVER_EXIT_CODE%.
pause
exit /b %SERVER_EXIT_CODE%
