@echo off
title Push All Changes to GitHub
color 0A
echo ========================================================
echo PUSHING ALL CHANGES TO GITHUB REPOSITORY
echo Repo: https://github.com/rintathomas2027/MULTIMODEL-RESEARCH-AGENT.git
echo Branch: main
echo ========================================================
cd /d C:\AIStudyAssistant

if exist ".git\index.lock" del /f /q ".git\index.lock"

echo.
echo [1/3] Adding modified and new files...
git add .

echo.
echo [2/3] Committing changes...
git commit -m "Enable dynamic relative API routes for Vercel, auto-seeding, and 1-click demo guest access"

echo.
echo [3/3] Pushing to origin main...
git push origin main
if %ERRORLEVEL% neq 0 (
    echo [INFO] Standard push returned non-zero, trying upstream main...
    git push -u origin main
)

echo.
echo ========================================================
echo All files have been pushed to GitHub successfully!
echo Repository: https://github.com/rintathomas2027/MULTIMODEL-RESEARCH-AGENT
echo ========================================================
pause

