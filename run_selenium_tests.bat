@echo off
setlocal
title ScholarPulse AI Studio - Selenium Automated Test Runner

cd /d "%~dp0"

echo ======================================================================
echo   ScholarPulse AI Studio - Selenium Automation Test Runner
echo ======================================================================
echo.

set "PYTHON_EXE=venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo Executing all 11 Selenium Automated Test Suites...
%PYTHON_EXE% run_selenium_tests.py

echo.
echo Opening Interactive Test Report in default browser...
start "" "reports\interactive_test_report.html"

echo.
echo Test Execution Finished!
pause
