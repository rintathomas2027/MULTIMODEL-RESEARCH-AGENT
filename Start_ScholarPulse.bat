@echo off
setlocal
title ScholarPulse AI

rem Always run from the folder that contains this launcher.
cd /d "%~dp0"

echo ==============================================
echo   ScholarPulse AI - starting local server
echo ==============================================

if not exist "venv\Scripts\python.exe" (
    echo.
    echo Python virtual environment was not found.
    echo Expected: %CD%\venv\Scripts\python.exe
    echo.
    pause
    exit /b 1
)

echo Updating the database schema...
"venv\Scripts\python.exe" manage.py migrate
if errorlevel 1 (
    echo.
    echo Database migration failed. See the error above.
    pause
    exit /b 1
)

echo Starting server at http://127.0.0.1:8000/
echo The browser will open when the server is ready.
echo Press Ctrl+C to stop the server.

rem Wait for Django to respond before opening the browser, avoiding a blank page.
start "ScholarPulse browser launcher" /b powershell -NoProfile -Command "$deadline=(Get-Date).AddSeconds(30); do { try { $response=Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:8000/' -TimeoutSec 2; if ($response.StatusCode -eq 200) { Start-Process 'http://127.0.0.1:8000/'; exit } } catch {}; Start-Sleep -Milliseconds 500 } while ((Get-Date) -lt $deadline)"

"venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
set "SERVER_EXIT_CODE=%ERRORLEVEL%"

echo.
echo Server stopped with exit code %SERVER_EXIT_CODE%.
pause
exit /b %SERVER_EXIT_CODE%
