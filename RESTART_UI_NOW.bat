@echo off
echo ========================================
echo RESTARTING CollTech-AGI with Dark Mode
echo ========================================
echo.
echo STEP 1: Close the current UI window completely
echo STEP 2: Press any key here to launch the new version
echo.
pause

cd /d "%~dp0"
python colltech_agi_chat_ui_expanded.py

pause
