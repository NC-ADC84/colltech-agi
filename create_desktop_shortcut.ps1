# PowerShell script to create a desktop shortcut for CollTech-AGI Chat UI

$WScriptShell = New-Object -ComObject WScript.Shell
$Desktop = [System.Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path $Desktop "CollTech-AGI Chat.lnk"
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)

# Get the current directory
$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Set shortcut properties
$Shortcut.TargetPath = "python.exe"
$Shortcut.Arguments = "`"$CurrentDir\colltech_agi_chat_ui.py`""
$Shortcut.WorkingDirectory = $CurrentDir
$Shortcut.Description = "CollTech-AGI Natural Language Chat Interface"
$Shortcut.WindowStyle = 1  # Normal window

# Save the shortcut
$Shortcut.Save()

Write-Host "✅ Desktop shortcut created successfully!" -ForegroundColor Green
Write-Host "Location: $ShortcutPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now double-click 'CollTech-AGI Chat' on your desktop to launch the chat UI!" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"
