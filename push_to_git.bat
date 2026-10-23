@echo off
title Push All Changes to GitHub (Zero Data Loss)
color 0A
echo ========================================================
echo PUSHING ALL CHANGES TO GITHUB REPOSITORY
echo Repo: https://github.com/rintathomas2027/MULTIMODEL-RESEARCH-AGENT.git
echo Branch: main
echo ========================================================
cd /d C:\AIStudyAssistant

if exist ".git\index.lock" del /f /q ".git\index.lock"

echo.
echo [Step 1/4] Safely exporting database records to data_dump.json...
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe export_sqlite_data.py
) else (
    python export_sqlite_data.py
)

echo.
echo [Step 2/4] Staging all files, media documents, and embeddings...
git add .

echo.
echo [Step 3/4] Committing changes...
git commit -m "Fix in-app Back navigation to prevent leaving site and preserve all features"

echo.
echo [Step 4/4] Pushing to origin main...
git push origin main
if %ERRORLEVEL% neq 0 (
    echo [INFO] Standard push returned non-zero, trying upstream main...
    git push -u origin main
)

echo.
echo ========================================================
echo All files, database, and media pushed to GitHub successfully!
echo Repository: https://github.com/rintathomas2027/MULTIMODEL-RESEARCH-AGENT
echo ========================================================
pause
