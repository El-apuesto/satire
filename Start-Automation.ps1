# OK Crisis News Automation Launcher
# Double-click to start both server and generator

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start Flask server in new window
Start-Process cmd -ArgumentList "/k", "cd /d `"$ScriptDir\crisis-display`"; python app.py" -WindowStyle Normal

# Wait for server to start
Start-Sleep -Seconds 5

# Start generator in new window  
Start-Process cmd -ArgumentList "/k", "cd /d `"$ScriptDir\crisis-generator`"; python full_automation.py --mode once" -WindowStyle Normal

Write-Host "Automation started!"
Write-Host "- Display Server: http://localhost:5000"
Write-Host "- Generator: Running in separate window"
Read-Host "Press Enter to exit..."
