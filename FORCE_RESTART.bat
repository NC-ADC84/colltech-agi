@echo off
echo ========================================
echo FORCE RESTARTING CollTech-AGI
echo ========================================
echo.
echo Killing any running Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo Clearing Python cache...
cd /d "%~dp0"
if exist __pycache__ rmdir /s /q __pycache__
if exist *.pyc del /q *.pyc

echo.
echo Launching fresh instance...
python colltech_agi_chat_ui_expanded.py

pause
