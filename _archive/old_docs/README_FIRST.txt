================================================================================
                    MAYA 2026 USD - YOU'RE ALMOST THERE!
================================================================================

STATUS: Everything is installed and all scripts are ready!

The warning about "pxr module" is NORMAL - you just need to enable the
MayaUSD plugin in Maya (one-time setup, takes 30 seconds).

================================================================================
DO THIS NOW (ONE TIME ONLY):
================================================================================

1. Launch Maya 2026

2. Go to: Windows > Settings/Preferences > Plug-in Manager

3. Find: mayaUsdPlugin.mll

4. Check BOTH boxes:
   [X] Loaded
   [X] Auto Load

5. Done! Close Maya.

================================================================================
WHAT THIS DOES:
================================================================================

When you enable mayaUsdPlugin.mll, it:
- Makes the pxr Python module available
- Sets up USD_LOCATION environment variable  
- Enables UsdView integration
- Allows USD import/export in Maya

================================================================================
VERIFY IT WORKED:
================================================================================

Run this again:
   C:\openusd-live-control\scripts\verify_maya.bat

You should now see:
   [OK] USD Python module (pxr) imports successfully

Instead of the warning you saw before.

================================================================================
THEN TEST THE SYSTEM:
================================================================================

Terminal 1:
   cd C:\openusd-live-control
   scripts\run_maya.bat

In Maya Script Editor (Python tab):
   exec(open(r'C:\openusd-live-control\tools\maya_bridge.py').read())

Terminal 2:
   cd C:\openusd-live-control
   call scripts\env_maya.bat
   python scripts\send_cmd.py set_pose /World/Robot 2 0 0 0 45 0

Result: Robot moves instantly in Maya!

================================================================================
FULL GUIDE: See FIRST_TIME_SETUP.md for detailed instructions
================================================================================

