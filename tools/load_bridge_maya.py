"""
Simple bridge loader for Maya Script Editor
Copy and paste this entire file into Maya Script Editor (Python tab) and press Ctrl+Enter

This avoids the exec() indentation issues.
"""

import sys
import os

# Add tools directory to Python path
tools_dir = r'C:\openusd-live-control\tools'
if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

# Import and start the bridge
try:
    # If already imported, reload it
    if 'maya_bridge' in sys.modules:
        import importlib
        import maya_bridge
        importlib.reload(maya_bridge)
        print("[loader] Bridge reloaded")
    else:
        import maya_bridge
        print("[loader] Bridge loaded for first time")
    
    print("[loader] Maya bridge is ready!")
    
except Exception as e:
    print(f"[loader] ERROR: {e}")
    import traceback
    traceback.print_exc()

