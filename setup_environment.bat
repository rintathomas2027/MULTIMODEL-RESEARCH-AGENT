@echo off
setlocal enabledelayedexpansion
title ScholarPulse AI Studio - Environment Setup

cd /d "%~dp0"

echo ======================================================================
echo   ScholarPulse AI Studio - 1-Click Automated Environment Setup
echo ======================================================================
echo.

rem 1. Check Python installation
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.10+ from https://python.org/
    pause
    exit /b 1
)

echo [1/5] Checking Python Virtual Environment...
if not exist "venv\Scripts\python.exe" (
    echo Creating fresh Python virtual environment in .\venv...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

echo.
echo [2/5] Installing Required Dependencies...
"venv\Scripts\python.exe" -m pip install --upgrade pip
"venv\Scripts\python.exe" -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Some dependencies had warnings during install. Proceeding...
)

echo.
echo [3/5] Setting Up Environment Configuration (.env)...
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo Created default .env file from .env.example.
    )
)

echo.
echo [4/5] Applying Database Migrations...
"venv\Scripts\python.exe" manage.py makemigrations users
"venv\Scripts\python.exe" manage.py makemigrations assistant
"venv\Scripts\python.exe" manage.py migrate

echo.
echo [5/5] Seeding Demo Research Papers & Vector Store...
"venv\Scripts\python.exe" seed_demo_data.py

echo.
echo ======================================================================
echo   SUCCESS! ScholarPulse AI Studio is fully configured.
echo ======================================================================
echo.
echo You can now run:
echo   - run_server.bat         : Start the web application
echo   - run_selenium_tests.bat : Run automated Selenium test suites
echo.
pause
