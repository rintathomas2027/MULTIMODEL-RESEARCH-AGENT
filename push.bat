@echo off
title Push Full Commit History to GitHub
color 0A
echo ========================================================
echo AUTOMATED MULTI-COMMIT GENERATOR & PUSH SCRIPT
echo Target Repo: https://github.com/rintathomas2027/MULTIMODEL-RESEARCH-AGENT.git
echo ========================================================
cd /d C:\AIStudyAssistant

echo.
if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" build_74_commits.py
) else (
    python build_74_commits.py
)

echo.
echo ========================================================
echo SUCCESS! Check https://github.com/rintathomas2027/MULTIMODEL-RESEARCH-AGENT
echo ========================================================
pause
