@echo off
title ScholarPulse AI Studio - Traditional Live Selenium Test
color 0A

echo ========================================================
echo   ScholarPulse AI Studio - Live Selenium Browser Test
echo ========================================================
echo.
echo NOTE: Make sure the local server is running at http://127.0.0.1:8000/
echo.
echo Running Traditional Live Selenium Test in Visible Chrome...
echo (You will see the browser open and perform actions automatically)
echo.

set "PYTHON_EXE=venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

%PYTHON_EXE% traditional_selenium_demo.py

echo.
echo ========================================================
echo Test Finished! Screenshot saved in reports\screenshots\
echo ========================================================
pause
