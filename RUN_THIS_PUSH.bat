@echo off
title Generate 74+ Commits & Push to GitHub
color 0A
echo ========================================================
echo AUTOMATED 74+ MULTI-COMMIT GENERATOR & PUSH SCRIPT
echo Repository: https://github.com/rintathomas2027/MULTIMODEL-RESEARCH-AGENT.git
echo ========================================================
cd /d C:\AIStudyAssistant

echo.
echo Running Python commit builder script...
python build_74_commits.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Python runner encountered an issue. Falling back to batch runner...
    python -c "import build_74_commits; build_74_commits.main()"
)

echo.
echo ========================================================
echo SUCCESS! Check https://github.com/rintathomas2027/MULTIMODEL-RESEARCH-AGENT
echo ========================================================
pause
