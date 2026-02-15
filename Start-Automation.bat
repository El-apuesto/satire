@echo off
echo Starting OK Crisis News Automation...
echo.

REM Start Flask server in first terminal
start "Crisis Display Server" cmd /k "cd /d %~dp0crisis-display && python app.py"

REM Wait for server to start
timeout /t 5 /nobreak >nul

REM Start generator in second terminal
start "Crisis Generator" cmd /k "cd /d %~dp0crisis-generator && python full_automation.py --mode once"

echo.
echo Automation started!
echo - Display Server: http://localhost:5000
echo - Generator: Running in separate window
echo.
pause
