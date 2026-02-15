# OK Crisis News Automation Launcher
# Double-click to start both server and generator

# Start Flask server in new window
Start-Process cmd -ArgumentList "/k", "cd /d `"$PSScriptRoot\crisis-display`"; python app.py" -WindowStyle Normal -WindowTitle "Crisis Display Server"

# Wait for server to start
Start-Sleep -Seconds 5

# Start generator in new window  
Start-Process cmd -ArgumentList "/k", "cd /d `"$PSScriptRoot\crisis-generator`"; python full_automation.py --mode once" -WindowStyle Normal -WindowTitle "Crisis Generator"

Write-Host "Automation started!"
Write-Host "- Display Server: http://localhost:5000"
Write-Host "- Generator: Running in separate window"
Read-Host "Press Enter to exit..."
