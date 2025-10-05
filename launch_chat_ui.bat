@echo off
REM CollTech-AGI Chat UI Launcher
REM Double-click this file to launch the chat interface

echo Starting CollTech-AGI Chat UI...
echo.

cd /d "%~dp0"
python colltech_agi_chat_ui.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start chat UI
    echo Make sure Python is installed and in your PATH
    pause
)
