# First Time Setup for Maya 2026 USD Live Control

## ✅ What You Have

- **Maya 2026** installed at `C:\Program Files\Autodesk\Maya2026`
- **MayaUSD 0.33.0** installed at `C:\Program Files\Autodesk\MayaUSD\Maya2026\0.33.0`
- USD versions available: 0.24.11 and 0.25.5
- All scripts ready to use!

## 🎯 Critical First Step: Enable MayaUSD Plugin

The `pxr` module warning you saw is **normal** - it just means the MayaUSD plugin isn't enabled yet. This is a one-time setup:

### Step 1: Launch Maya
```batch
"C:\Program Files\Autodesk\Maya2026\bin\maya.exe"
```

### Step 2: Enable MayaUSD Plugin

1. In Maya, go to: **Windows → Settings/Preferences → Plug-in Manager**
2. Scroll down and find: `mayaUsdPlugin.mll`
3. Check **BOTH** boxes:
   - ✅ **Loaded** (enables it now)
   - ✅ **Auto Load** (enables it every time Maya starts)
4. You should see a message in the Script Editor confirming the plugin loaded

### Step 3: Verify It Works

In Maya's Script Editor (Python tab), run:
```python
from pxr import Usd
print("USD version:", Usd.GetVersion())
```

If this prints a version number (like `(0, 24, 11)`), **you're good to go!**

## 🚀 Now Test the Live Control System

### Terminal 1: Launch Maya with Scene
```batch
cd C:\openusd-live-control
scripts\run_maya.bat
```

Maya opens with `world.usda` loaded.

### In Maya: Load the Bridge

In Script Editor (Python tab):
```python
exec(open(r'C:\openusd-live-control\tools\maya_bridge.py').read())
```

Wait for the message:
```
[maya-bridge] Listening on 127.0.0.1:8765
```

### Terminal 2: Send Test Command
```batch
cd C:\openusd-live-control
call scripts\env_maya.bat
python scripts\send_cmd.py set_pose /World/Robot 2 0 0 0 45 0
```

**Expected**: Robot moves in Maya viewport instantly! 🎉

## 📋 Testing Checklist

After enabling the plugin, run verification again:
```batch
cd C:\openusd-live-control\scripts
verify_maya.bat
```

You should now see:
```
[OK] Found Maya 2026
[OK] maya.exe found
[OK] mayapy.exe found
[OK] MayaUSD installation directory found
[OK] USD Python module (pxr) imports successfully  ← This was the warning before!
```

## 🎬 Test UsdView Integration

Once the plugin is enabled, you can launch UsdView from Maya:

1. In Maya, open or import a USD file
2. Select a USD prim in the viewport
3. In Script Editor (Python tab):
   ```python
   exec(open(r'C:\openusd-live-control\scripts\maya_usdview_shelf.py').read())
   ```

UsdView launches showing your USD scene!

## 📖 Understanding What Happened

### Why the Warning About `pxr` Module?

The MayaUSD plugin isn't just files on disk - it's a Maya plugin that must be **loaded** in Maya. When loaded, it:
- Sets the `USD_LOCATION` environment variable
- Makes the `pxr` Python module available
- Enables USD import/export in Maya
- Provides UsdView integration

### Why Enable "Auto Load"?

Without "Auto Load", you'd have to manually enable the plugin every time you start Maya. With it checked, Maya loads it automatically.

## 🔧 Troubleshooting

### "mayaUsdPlugin.mll not found in Plug-in Manager"

Try refreshing the plugin list:
- Close and reopen the Plug-in Manager
- Or restart Maya

### "Plugin failed to load"

Check the Script Editor for error messages. Common issues:
- Missing Visual C++ redistributables
- Conflicting USD installations in system PATH

### Still Can't Import pxr?

The `pxr` module is only available:
1. **Inside Maya** after loading the plugin
2. **Via mayapy** after the plugin has been loaded in Maya at least once

It won't work in regular Python - you must use Maya's bundled Python.

## ✅ Next Steps

Once the plugin is enabled:
1. ✅ Run `verify_maya.bat` again - should be all green
2. ✅ Test the live control system (see above)
3. ✅ Try all 8 commands
4. ✅ Test UsdView integration
5. ✅ Build your USD pipeline!

## 📚 Official Resources

- **Maya USD Docs**: https://help.autodesk.com/view/MAYACRE/ENU/
- **MayaUSD GitHub**: https://github.com/Autodesk/maya-usd
- **USD Glossary**: Pixar USD documentation

---

**The ONE thing you need to do**: Enable `mayaUsdPlugin.mll` in Maya's Plug-in Manager. Everything else is ready! 🎯

