"""
Launch UsdView from Maya - Shelf Button Script
Based on official Autodesk MayaUSD documentation

USAGE:
1. In Maya, select a USD prim in the viewport
2. Run this script from Script Editor (Python tab)
3. UsdView will launch showing the selected USD asset

OR add to shelf:
- Select this entire script text
- Middle-mouse drag to Maya shelf
- Click the shelf button whenever you want to launch UsdView
"""

import maya.cmds as cmds
import ufe
from pxr import Usd
import mayaUsd as uLib
import os
import sys
import subprocess

def launch_usdview():
    """Launch UsdView for the currently selected USD asset in Maya"""
    
    # Check if something is selected
    if ufe.GlobalSelection.get().empty():
        cmds.error('Please select a USD prim in the viewport first!\n'
                   'Select any USD object (under the USD gateway node) and try again.')
        return
    
    # Get the selected UFE item
    ufeItem = ufe.GlobalSelection.get().back()
    
    # Get the USD stage (using official Autodesk syntax for Maya 2026)
    try:
        stage = uLib.ufe.getStage(ufe.PathString.string(ufeItem.path()))
    except Exception as e:
        cmds.error(f'Could not get USD stage from selection: {e}')
        return
    
    # Get the root layer
    sdfLayer = stage.GetRootLayer()
    
    # Check if it has a concrete file path (not anonymous layer)
    if not sdfLayer.realPath:
        cmds.error('Selected USD item does not have a concrete file path.\n'
                   'It may be an anonymous layer. Try selecting a different USD prim.')
        return
    
    # Get Maya version
    mayaVer = int(cmds.about(q=True, majorVersion=True))
    
    # Build path to mayapy
    mayapyBinPath = os.path.join(os.environ['MAYA_LOCATION'], 'bin')
    
    # Handle Maya 2022 which has both Python 2 and 3
    if mayaVer == 2022:
        mayapyPath = os.path.join(mayapyBinPath, 'mayapy{ver}'.format(
            ver='' if sys.version_info.major == 3 else '2'))
    else:
        mayapyPath = os.path.join(mayapyBinPath, 'mayapy')
    
    # Get USD location
    if 'USD_LOCATION' not in os.environ:
        cmds.error('USD_LOCATION environment variable not set!\n'
                   'MayaUSD may not be properly configured.')
        return
    
    usdRootPath = os.environ['USD_LOCATION']
    
    # Sanitize path separators
    mayapyPath = mayapyPath.replace('\\', os.path.sep).replace('/', os.path.sep)
    usdRootPath = usdRootPath.replace('\\', os.path.sep).replace('/', os.path.sep)
    sdfLayerPath = sdfLayer.realPath.replace('\\', os.path.sep).replace('/', os.path.sep)
    
    # Build paths to USD tools
    usdToolsPath = os.path.join(usdRootPath, "bin")
    usdLibPath = os.path.join(usdRootPath, "lib")
    usdViewPath = os.path.join(usdToolsPath, 'usdview')
    
    # Check if mayapy exists
    if not os.path.exists(mayapyPath):
        cmds.error(f'mayapy not found at: {mayapyPath}')
        return
    
    # Check if usdview exists
    if not os.path.exists(usdViewPath) and not os.path.exists(usdViewPath + '.py'):
        cmds.error(f'usdview not found at: {usdViewPath}\n'
                   f'USD tools path: {usdToolsPath}')
        return
    
    # Install PyOpenGL if needed (required by UsdView)
    try:
        import OpenGL
        print("[UsdView] PyOpenGL already installed")
    except ImportError:
        print("[UsdView] Installing PyOpenGL...")
        try:
            subprocess.check_call([mayapyPath, '-m', 'pip', 'install', 'PyOpenGL==3.1.0'])
            print("[UsdView] PyOpenGL installed successfully")
        except subprocess.CalledProcessError as e:
            cmds.warning(f'Could not install PyOpenGL: {e}\n'
                        'UsdView may not launch correctly.')
    
    # Set creation flags for Windows (suppress console window)
    if sys.platform in ('win32'):
        creationflags = 0x08000000  # CREATE_NO_WINDOW
    else:
        creationflags = 0
    
    # Build command
    command = [mayapyPath, usdViewPath, sdfLayerPath]
    
    print("="*60)
    print("[UsdView] Launching UsdView...")
    print(f"[UsdView] USD File: {sdfLayerPath}")
    print(f"[UsdView] Command: {' '.join(command)}")
    print("="*60)
    
    # Launch UsdView
    try:
        subprocess.Popen(command, creationflags=creationflags)
        print("[UsdView] UsdView launched successfully!")
        print("[UsdView] Check for UsdView window on your desktop")
    except Exception as e:
        cmds.error(f'Failed to launch UsdView: {e}')

# Run the function when script is executed
if __name__ == '__main__' or __name__ == 'builtins':
    launch_usdview()

