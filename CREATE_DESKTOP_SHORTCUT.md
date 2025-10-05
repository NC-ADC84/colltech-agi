# 🖥️ Create Desktop Shortcut

## Quick Method (Easiest)

### Option 1: Right-Click Method
1. Navigate to the `colltech-agi` folder
2. Find `launch_chat_ui.bat`
3. Right-click on it
4. Select "Send to" → "Desktop (create shortcut)"
5. Done! Double-click the shortcut on your desktop to launch

### Option 2: PowerShell Script (Automatic)
1. Navigate to the `colltech-agi` folder
2. Right-click on `create_desktop_shortcut.ps1`
3. Select "Run with PowerShell"
4. If you get a security warning, type `Y` and press Enter
5. Done! The shortcut will be created automatically

### Option 3: Manual Shortcut Creation
1. Right-click on your Desktop
2. Select "New" → "Shortcut"
3. For location, enter:
   ```
   python.exe "C:\Users\Andre\OneDrive - Andre Collier\Shared\shared\colltech-agi\colltech_agi_chat_ui.py"
   ```
   (Adjust the path to match your actual location)
4. Click "Next"
5. Name it "CollTech-AGI Chat"
6. Click "Finish"

---

## 🎨 Customize Your Shortcut

### Change the Icon
1. Right-click on the shortcut
2. Select "Properties"
3. Click "Change Icon"
4. Browse to find an icon you like
5. Click "OK"

### Change the Name
1. Right-click on the shortcut
2. Select "Rename"
3. Type your preferred name
4. Press Enter

---

## ✅ Verify It Works

1. Double-click your new desktop shortcut
2. The CollTech-AGI Chat window should open
3. You should see the welcome message
4. Try sending a test message

---

## 🚀 You're All Set!

Now you can launch CollTech-AGI Chat directly from your desktop with a single double-click!

For help using the chat interface, see `CHAT_UI_GUIDE.md`
