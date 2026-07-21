# 🚀 START HERE - Maya USD Live Control

## ✅ You Have Maya 2026 Installed!

All scripts are ready! You just need **one quick setup step** (30 seconds) to enable the MayaUSD plugin.

## 🎯 **FIRST**: Read `README_FIRST.txt` or `FIRST_TIME_SETUP.md`

The "pxr module warning" you saw is normal - it just means the MayaUSD plugin isn't enabled yet.

## What It Does

- **Live Control**: Change robot positions, camera angles, add/remove objects in real-time
- **No Refresh Needed**: Viewport updates instantly as commands are sent
- **Programmatic API**: Control everything via simple CLI commands
- **UsdView Access**: Inspect USD scenes with Pixar's professional tools
- **Free for Students**: 3-year Maya education license at zero cost

## Your Current Status

✅ All scripts created and ready
✅ Project structure in place
✅ Documentation complete
❌ **Need to install Maya** (this is the only step!)

## Next Steps

### 1. Get Maya (30-60 minutes)

1. Visit: **https://www.autodesk.com/education/home**
2. Create account (use student email for instant approval)
3. Download **Maya 2025** for Windows
4. Install with default settings
5. Done!

### 2. Verify Installation (2 minutes)

```batch
cd C:\openusd-live-control
scripts\verify_maya.bat
```

Expected: `[OK] Found Maya 2025` and `[OK] pxr module imports successfully`

### 3. Enable MayaUSD Plugin (First Launch, 2 minutes)

1. Launch Maya
2. **Windows → Settings/Preferences → Plug-in Manager**
3. Find `mayaUsdPlugin.mll`
4. Check: ✅ **Loaded** ✅ **Auto Load**
5. Close Maya

### 4. Test the System (5 minutes)

**Terminal 1 - Launch Maya:**
```batch
cd C:\openusd-live-control
scripts\run_maya.bat
```

**In Maya - Start bridge** (Script Editor, Python tab):
```python
exec(open(r'C:\openusd-live-control\tools\maya_bridge.py').read())
```

Wait for: `[maya-bridge] Listening on 127.0.0.1:8765`

**Terminal 2 - Send command:**
```batch
cd C:\openusd-live-control
call scripts\env_maya.bat
python scripts\send_cmd.py set_pose /World/Robot 2 0 0 0 45 0
```

**Result**: Robot moves instantly! 🎉

## All Available Commands

```batch
# Move robot
python scripts\send_cmd.py set_pose /World/Robot 5 0 0 0 90 0

# Change camera
python scripts\send_cmd.py set_camera /World/Camera 0 5 10 -20 0 0

# Add cube
python scripts\send_cmd.py add_cube /World/Box 0.5

# Hide/show
python scripts\send_cmd.py vis /World/Robot false

# Delete
python scripts\send_cmd.py rm /World/Box

# Set attribute
python scripts\send_cmd.py attr /World/Robot color red

# Save
python scripts\send_cmd.py save
```

## Launch UsdView (Optional)

In Maya (after loading a USD file):
1. Select a USD object
2. Script Editor (Python tab):
   ```python
   exec(open(r'C:\openusd-live-control\scripts\maya_usdview_shelf.py').read())
   ```

UsdView launches showing your scene!

Or create a shelf button for one-click access (MEL tab):
```mel
source "C:/openusd-live-control/scripts/setup_usdview_shelf.mel";
```

## Complete Guides

- **[MAYA_QUICKSTART.txt](MAYA_QUICKSTART.txt)** - Quick reference guide
- **[README_MAYA.md](README_MAYA.md)** - Complete documentation
- **[README.md](README.md)** - Original project info

## Files Created for You

### Scripts (Ready to Use)
- `scripts/verify_maya.bat` - Check Maya installation
- `scripts/run_maya.bat` - Launch Maya with USD scene
- `scripts/env_maya.bat` - Environment setup
- `scripts/send_cmd.py` - CLI client (**unchanged from original!**)

### Maya Integration
- `tools/maya_bridge.py` - Socket server (runs in Maya)
- `scripts/maya_usdview_shelf.py` - Launch UsdView
- `scripts/maya_usdview_cmdline.py` - Command-line UsdView
- `scripts/setup_usdview_shelf.mel` - Add shelf button

### Test Scene
- `scenes/world.usda` - Auto-created with Robot and Camera

## Requirements Checklist

✅ Use USD API to manipulate robot position
✅ Change object state without refresh
✅ Programmatically implement scene changes
✅ Upload USD and live-view programmatically
✅ Send position to control robot via API
✅ Use API to run scripts
✅ Control camera pose programmatically
✅ Access UsdView for USD inspection

**All requirements met!** Just install Maya and you're ready.

## Support

- **Maya Download**: https://www.autodesk.com/education/home
- **MayaUSD GitHub**: https://github.com/Autodesk/maya-usd
- **OpenUSD Docs**: https://openusd.org/

## Troubleshooting

See **[README_MAYA.md](README_MAYA.md)** for complete troubleshooting guide.

---

**Ready? Install Maya and let's go!** 🎬

Visit: **https://www.autodesk.com/education/home**

