# Maya USD Live Control - Complete Guide

Real-time USD scene manipulation using Maya's robust command port and MayaUSD plugin.

## Why Maya?

- **Free for Students** (3-year education license)
- **Reliable Command Port** (battle-tested in production)
- **MayaUSD Integration** (official Pixar/Autodesk/NVIDIA collaboration)
- **UsdView Access** (inspect USD scenes with Pixar's tools)
- **Industry Standard** (valuable skills for VFX/animation/robotics)

## Prerequisites

✅ Windows 11
✅ Student email for Autodesk Education account
✅ ~12 GB disk space for Maya
✅ Existing `openusd-live-control` repository

## Quick Start (After Maya is Installed)

### Terminal 1: Launch Maya with USD Scene
```batch
cd C:\openusd-live-control
scripts\run_maya.bat
```

Maya opens with `scenes\world.usda` loaded.

### In Maya Script Editor (Python tab):
```python
exec(open(r'C:\openusd-live-control\tools\maya_bridge.py').read())
```

You should see:
```
[maya-bridge] Listening on 127.0.0.1:8765
[maya-bridge] Ready to receive commands from send_cmd.py
```

### Terminal 2: Send Commands
```batch
cd C:\openusd-live-control
call scripts\env_maya.bat
python scripts\send_cmd.py set_pose /World/Robot 2 0 0 0 45 0
```

**Result**: Robot moves instantly in Maya viewport! 🎉

---

## Installation Guide

### Step 1: Get Maya (Student License)

1. Go to: https://www.autodesk.com/education/home
2. Click "Get Started" → Create account
3. Verify student status (use .edu email or upload student ID)
4. Download **Maya 2025** (or latest version)
5. Run installer (~20 minutes)
6. **Important**: Accept all default components (includes MayaUSD)

### Step 2: Verify Installation

Run verification script:
```batch
cd C:\openusd-live-control
scripts\verify_maya.bat
```

Expected output:
```
[OK] Found Maya 2025
[OK] maya.exe found
[OK] mayapy.exe found
[OK] MayaUSD.mod file found
```

### Step 3: Enable MayaUSD Plugin (First Launch Only)

1. Launch Maya
2. Go to: **Windows → Settings/Preferences → Plug-in Manager**
3. Find `mayaUsdPlugin.mll`
4. Check **both** boxes:
   - ✅ Loaded
   - ✅ Auto Load
5. Verify in Script Editor (Python tab):
   ```python
   import maya.cmds as cmds
   print(cmds.pluginInfo('mayaUsdPlugin', query=True, loaded=True))
   # Should print: True
   ```

---

## Usage

### Method 1: Manual Bridge Start (Recommended for Learning)

1. **Launch Maya**:
   ```batch
   scripts\run_maya.bat
   ```

2. **Start Bridge** (in Maya Script Editor - Python tab):
   ```python
   exec(open(r'C:\openusd-live-control\tools\maya_bridge.py').read())
   ```

3. **Send Commands** (from Windows terminal):
   ```batch
   python scripts\send_cmd.py set_pose /World/Robot 2 0 0 0 45 0
   ```

### Method 2: Auto-Start Bridge (Optional)

Copy `scripts\run_maya_with_bridge.mel` to your Maya scripts folder:
```batch
copy scripts\run_maya_with_bridge.mel "%USERPROFILE%\Documents\maya\2025\scripts\userSetup.mel"
```

Now the bridge auto-loads every time Maya starts!

---

## Commands Reference

All commands work the same as the original `openusd-live-control`:

### 1. Set Pose (Position/Rotation/Scale)
```batch
python scripts\send_cmd.py set_pose /World/Robot 2 0 0 0 45 0
# Moves Robot to x=2, rotates 45° on Y-axis
```

### 2. Set Camera
```batch
python scripts\send_cmd.py set_camera /World/Camera 0 5 10 -20 0 0
# Camera at (0,5,10), looking down 20°
```

### 3. Add Cube
```batch
python scripts\send_cmd.py add_cube /World/Box 0.5
# Creates 0.5-unit cube named "Box"
```

### 4. Toggle Visibility
```batch
python scripts\send_cmd.py vis /World/Robot false
python scripts\send_cmd.py vis /World/Robot true
```

### 5. Remove Object
```batch
python scripts\send_cmd.py rm /World/Box
```

### 6. Set Attribute
```batch
python scripts\send_cmd.py attr /World/Robot color "red"
```

### 7. Open USD File
```batch
python scripts\send_cmd.py open "C:\path\to\scene.usda"
```

### 8. Save
```batch
python scripts\send_cmd.py save
```

---

## UsdView Integration

Maya includes UsdView (Pixar's USD inspection tool) for debugging and exploring USD scenes.

### Launch UsdView from Maya

**Method 1: Python Script**

1. Load a USD file in Maya
2. Select a USD prim in the viewport
3. In Script Editor (Python tab), run:
   ```python
   exec(open(r'C:\openusd-live-control\scripts\maya_usdview_shelf.py').read())
   ```

UsdView launches showing your USD scene!

**Method 2: Shelf Button (One-Time Setup)**

1. In Script Editor (MEL tab), run:
   ```mel
   source "C:/openusd-live-control/scripts/setup_usdview_shelf.mel";
   ```

2. A "UsdView" button appears on your shelf
3. Click it anytime to launch UsdView for selected USD prim

### UsdView from Command Line

**Get the environment paths**:
1. In Maya Script Editor (Python tab):
   ```python
   exec(open(r'C:\openusd-live-control\scripts\maya_usdview_cmdline.py').read())
   ```

2. A command prompt opens with correct PATH
3. Run UsdView:
   ```batch
   mayapy usdview C:\openusd-live-control\scenes\world.usda
   ```

---

## Round-Trip Workflow Example

This demonstrates the full power of Maya + UsdView + Live Control:

1. **Start Maya with bridge**:
   ```batch
   scripts\run_maya.bat
   # In Maya: exec(open(r'tools\maya_bridge.py').read())
   ```

2. **Modify scene via API**:
   ```batch
   python scripts\send_cmd.py set_pose /World/Robot 5 0 0 0 90 0
   python scripts\send_cmd.py add_cube /World/Platform 10
   python scripts\send_cmd.py set_camera /World/Camera -10 10 10 -30 -30 0
   ```

3. **Inspect in UsdView**:
   - In Maya, select a USD prim
   - Run `maya_usdview_shelf.py` script
   - UsdView opens → explore USD hierarchy, attributes, composition arcs

4. **Save and iterate**:
   ```batch
   python scripts\send_cmd.py save
   ```

---

## Troubleshooting

### Maya Bridge Won't Start

**Symptom**: No "[maya-bridge] Listening..." message

**Solutions**:
- Check if another process is using port 8765:
  ```batch
  netstat -ano | findstr 8765
  ```
- Restart Maya and try again
- Check Maya Script Editor for Python errors

### Commands Return "Object not found"

**Symptom**: `{"ok": false, "error": "Object not found: /World/Robot"}`

**Solutions**:
- Make sure USD file is loaded in Maya
- Check object names in Maya Outliner
- USD paths are case-sensitive
- Try using Maya object names instead of USD paths

### UsdView Won't Launch

**Symptom**: Script runs but UsdView doesn't appear

**Solutions**:
- Check if you selected a USD prim first
- Verify USD_LOCATION is set (run `maya_usdview_cmdline.py` to check)
- Install PyOpenGL manually:
  ```batch
  "C:\Program Files\Autodesk\Maya2025\bin\mayapy.exe" -m pip install PyOpenGL==3.1.0
  ```

### MayaUSD Plugin Not Loading

**Symptom**: `mayaUsdPlugin.mll not found in Plug-in Manager`

**Solutions**:
- Check if MayaUSD is installed:
  ```batch
  dir "C:\Program Files\Autodesk\MayaUSD"
  dir "C:\Program Files\Common Files\Autodesk Shared\Modules\Maya"
  ```
- Download latest MayaUSD from: https://github.com/Autodesk/maya-usd/releases
- Reinstall Maya with all components

---

## Project Structure

```
C:\openusd-live-control\
├── scripts\
│   ├── env_maya.bat                 # Maya environment setup
│   ├── run_maya.bat                 # Launch Maya with USD scene
│   ├── run_maya_with_bridge.mel     # Auto-start bridge (optional)
│   ├── verify_maya.bat              # Installation verification
│   ├── maya_usdview_shelf.py        # Launch UsdView from Maya
│   ├── maya_usdview_cmdline.py      # UsdView command-line setup
│   ├── setup_usdview_shelf.mel      # Create UsdView shelf button
│   └── send_cmd.py                  # CLI client (UNCHANGED!)
├── tools\
│   ├── maya_bridge.py               # NEW: Maya command port server
│   └── usdview_bridge.py            # OLD: For reference
├── scenes\
│   └── world.usda                   # Test scene (auto-created)
├── third_party\                     # USD resources/examples
└── logs\                            # Logs and verification output
```

---

## Architecture

```
Terminal                                Maya
   │                                      │
   │   python send_cmd.py                │
   │   set_pose /Robot 2 0 0 0 45 0      │
   │                                      │
   └──────> Socket 127.0.0.1:8765 ───────┤
                                          │
                                    maya_bridge.py
                                          │
                                    maya.cmds API
                                          │
                                    MayaUSD Plugin
                                          │
                                    USD Stage (pxr)
                                          │
                                    Maya Viewport
                                    (LIVE UPDATE!)
```

---

## Requirements Checklist

✅ **USD API to manipulate robot position** - `set_pose` command
✅ **Change state without refresh** - Maya viewport updates live
✅ **Programmatic scene changes** - All 8 commands via socket API
✅ **Upload USD and live-view** - `open_stage` + real-time updates
✅ **Control robot programmatically** - `send_cmd.py` CLI
✅ **Upload/run scripts** - Python commands via maya.cmds
✅ **Control camera pose** - `set_camera` command
✅ **UsdView access** - Launch from Maya + command line

---

## Next Steps

1. **Download Maya** from Autodesk Education (student license)
2. **Install Maya** with default components
3. **Run `verify_maya.bat`** to check installation
4. **Enable MayaUSD** plugin in Plug-in Manager
5. **Test workflow**:
   - Run `run_maya.bat`
   - Load bridge in Script Editor
   - Send test command
6. **Add UsdView** shelf button for convenience
7. **Build your USD pipeline!**

---

## Support

- **MayaUSD Docs**: https://github.com/Autodesk/maya-usd
- **USD Docs**: https://openusd.org/
- **Maya Education**: https://www.autodesk.com/education/
- **Pixar UsdView**: Included with MayaUSD

---

**Happy USD controlling!** 🎬🤖

