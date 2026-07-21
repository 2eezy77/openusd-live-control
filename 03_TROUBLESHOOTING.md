# Troubleshooting Guide

Solutions for common issues with Maya USD Live Control.

---

## 🔧 Bridge Issues

### Bridge Won't Start

**Symptom:** No "Listening..." message in Maya

**Solutions:**

1. **Check Maya Script Editor for errors**
   - Look for red text in top panel
   - Common: Python syntax errors

2. **Verify MayaUSD plugin is loaded**
   - Windows → Plug-in Manager
   - Find `mayaUsdPlugin.mll`
   - Check both boxes: Loaded + Auto Load

3. **Make sure you're using Script Editor (not console)**
   - Console = single line at bottom of Maya ❌
   - Script Editor = separate window ✅
   - Windows → General Editors → Script Editor

4. **Verify Python tab is selected**
   - Click Python tab at top of Script Editor
   - NOT the MEL tab

5. **Check path is correct**
   ```python
   import os
   print(os.path.exists(r'C:\openusd-live-control\tools\maya_bridge.py'))
   # Should print: True
   ```

6. **Restart Maya completely**
   - Close Maya
   - Wait 10 seconds
   - Relaunch with `scripts\run_maya.bat`

---

### "Name 'sys' is not defined"

**Cause:** Running commands in wrong order

**Solution:** Always import sys first
```python
import sys
sys.path.append(r'C:\openusd-live-control\tools')
import maya_bridge
```

---

### "maya_bridge not found"

**Cause:** Path not added to sys.path

**Solution:** Make sure you run all 3 lines:
```python
import sys  # Line 1
sys.path.append(r'C:\openusd-live-control\tools')  # Line 2
import maya_bridge  # Line 3
```

---

### "Unexpected indent"

**Cause:** Spaces/tabs before commands

**Solution:**
1. Clear Script Editor (Ctrl+A, Delete)
2. Paste commands starting at column 0 (left edge)
3. No spaces before `import`

---

## 🔌 Connection Issues

### "Connection refused"

**Symptom:** Commands fail with connection error

**Solutions:**

1. **Bridge not running**
   - Check Maya Script Editor
   - Should see: `[maya-bridge] Listening on 127.0.0.1:8765`
   - If not, reload bridge

2. **Port already in use**
   ```batch
   netstat -ano | findstr 8765
   ```
   If something is using port 8765, restart Maya

3. **Wrong terminal directory**
   ```batch
   cd C:\openusd-live-control
   call scripts\env_maya.bat
   ```

---

### Commands are slow (>1 second)

**Causes:**
- Network issues
- Antivirus blocking Python
- Too many objects in scene

**Solutions:**
- Close other programs
- Check antivirus settings
- Restart Maya and bridge

---

## 📦 Object Issues

### "Object not found"

**Symptom:** `{"ok": false, "error": "Object not found: BoxName"}`

**Solutions:**

1. **Check exact name in Maya Outliner**
   - Names are case-sensitive!
   - Might be `Box1`, `Box2`, etc.

2. **List all objects**
   ```batch
   python scripts\send_cmd.py list_objects
   ```
   Use exact name from output

3. **Check object exists**
   - Look in Maya Outliner (Window → Outliner)
   - Select object, check name in Channel Box

4. **Object might have namespace**
   - Name might be `World:Box` instead of `Box`
   - Use full name with namespace

---

### Can't see created objects

**Solutions:**

1. **Position camera**
   ```batch
   python scripts\send_cmd.py set_camera persp 10 10 10 -30 30 0
   ```

2. **Move object up**
   ```batch
   python scripts\send_cmd.py set_pose ObjectName 0 5 0 0 0 0
   ```

3. **Press F in Maya**
   - Select object
   - Press `F` key (frame selected)

4. **Check viewport mode**
   - Press `4` for wireframe
   - Press `5` for shaded
   - Press `6` for textured

---

## 🎨 Color Issues

### Color doesn't change

**Symptom:** Command succeeds but no visible change

**Solutions:**

1. **Wrong viewport mode**
   - Press `6` in Maya viewport (hardware texturing)
   - Or press `7` for lighting mode

2. **Object doesn't exist**
   ```batch
   python scripts\send_cmd.py list_objects
   ```
   Verify object name

3. **Check override is enabled**
   In Maya Script Editor:
   ```python
   import maya.cmds as cmds
   print(cmds.getAttr("ObjectName.overrideEnabled"))
   # Should be 1
   ```

---

## 🎬 Animation Issues

### Animation doesn't play

**Solutions:**

1. **Check timeline range**
   ```batch
   python scripts\send_cmd.py get_time
   ```

2. **Set explicit range**
   ```batch
   python scripts\send_cmd.py play 1 120
   ```

3. **FBX might not have animation**
   - Check Graph Editor in Maya
   - Verify FBX has animation data

---

### Character doesn't move

**Solutions:**

1. **Find correct root node**
   - Check Maya Outliner after importing FBX
   - Try different node names (Hips, Root, etc.)

2. **Test with simple movement**
   ```batch
   python scripts\send_cmd.py set_pose NodeName 5 0 0 0 0 0
   ```

---

## 🏭 Warehouse Issues

### Can't load warehouse USD

**Solutions:**

1. **Check file exists**
   ```
   C:\openusd-live-control\scenes\warehouse_with_security_cameras (3).usd
   ```

2. **Use quotes for paths with spaces**
   ```batch
   python scripts\send_cmd.py open "C:\path\with spaces\file.usd"
   ```

3. **Try forward slashes**
   ```batch
   python scripts\send_cmd.py open "C:/openusd-live-control/scenes/warehouse.usd"
   ```

---

### Can't find warehouse objects

**Solution:** Use discovery script
```batch
python scripts\discover_warehouse.py
```
This lists all components with exact names.

---

## 🧪 Testing Issues

### Test script fails

**Solutions:**

1. **Make sure bridge is running first**
   - Load bridge in Maya
   - Wait for "Listening..." message

2. **Run from correct directory**
   ```batch
   cd C:\openusd-live-control
   call scripts\env_maya.bat
   python scripts\test_complete_system.py
   ```

3. **Check which test failed**
   - Script shows which test failed
   - Try that command manually
   - Check error message

---

## 🆘 Emergency Reset

**If everything is broken:**

1. **Close everything**
   - Close Maya
   - Close all terminals
   - Wait 10 seconds

2. **Fresh start**
   ```batch
   cd C:\openusd-live-control
   scripts\run_maya.bat
   ```

3. **In Maya Script Editor**
   ```python
   import sys
   sys.path.append(r'C:\openusd-live-control\tools')
   import maya_bridge
   ```

4. **Test connection**
   ```batch
   cd C:\openusd-live-control
   call scripts\env_maya.bat
   python scripts\send_cmd.py list_objects
   ```

---

## 📞 Diagnostic Commands

### Check connection
```batch
python scripts\send_cmd.py list_objects
```
Should return JSON with `{"ok": true}`

### Check object exists
```batch
python scripts\send_cmd.py list_objects
```
Look for object name in output

### Test simple command
```batch
python scripts\send_cmd.py add_cube /World/Test 2
```
Should create visible cube

### Check Maya version
In Maya Script Editor:
```python
import maya.cmds as cmds
print(cmds.about(version=True))
```

---

## ✅ Verification Checklist

- [ ] Maya opens from `run_maya.bat`
- [ ] Script Editor is separate window (not console)
- [ ] Python tab is selected
- [ ] Bridge shows "Listening on 127.0.0.1:8765"
- [ ] `list_objects` returns JSON
- [ ] `add_cube` creates visible cube
- [ ] `set_color` changes color in viewport
- [ ] All commands return `{"ok": true}`

**If all checked:** System is working! ✅

---

**Still stuck?** Check [01_COMPLETE_GUIDE.md](01_COMPLETE_GUIDE.md) for detailed explanations.

