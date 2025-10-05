@echo off
echo ========================================
echo CollTech-AGI Chat - 9 Personalities
echo ========================================
echo.
echo Starting expanded chat interface...
echo.

cd /d "%~dp0"
python colltech_agi_chat_ui_expanded.py

if errorlevel 1 (
    echo.
    echo Error launching chat interface!
    echo.
    pause
)
