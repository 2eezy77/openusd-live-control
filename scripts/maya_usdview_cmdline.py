"""
Setup Command Line Environment for UsdView
Based on official Autodesk MayaUSD documentation

USAGE:
1. Run this script from Maya Script Editor (Python tab)
2. It will print the required paths and open a command prompt
3. In the command prompt, you can run:
   mayapy usdview C:\path\to\scene.usda

This is useful for:
- Running UsdView from command line
- Debugging USD issues
- Running other USD command-line tools (usdcat, usddiff, etc.)
"""

import maya.cmds as cmds
import os
import sys
import subprocess

def setup_usdview_cmdline():
    """Print USD paths and launch a command shell with proper environment"""
    
    # Get Maya version
    mayaVer = int(cmds.about(q=True, majorVersion=True))
    
    # Build path to mayapy
    if mayaVer == 2022:
        mayapyPath = os.path.join(os.environ['MAYA_LOCATION'], 'bin', 
                                 'mayapy{ver}'.format(ver='' if sys.version_info.major == 3 else '2'))
    else:
        mayapyPath = os.path.join(os.environ['MAYA_LOCATION'], 'bin', 'mayapy')
    
    # Get USD location
    if 'USD_LOCATION' not in os.environ:
        cmds.error('USD_LOCATION environment variable not set!\n'
                   'MayaUSD may not be properly configured.')
        return
    
    usdRootPath = os.environ['USD_LOCATION']
    
    # Sanitize path separators
    mayapyPath = mayapyPath.replace('\\', os.path.sep).replace('/', os.path.sep)
    usdRootPath = usdRootPath.replace('\\', os.path.sep).replace('/', os.path.sep)
    
    # Build paths to USD tools and libraries
    usdToolsPath = os.path.join(usdRootPath, "bin")
    usdLibPath = os.path.join(usdRootPath, "lib")
    mayapyBinPath = os.path.dirname(mayapyPath)
    
    # Path divider (Windows vs Unix)
    path_divider = ";" if sys.platform in ('win32') else ":"
    
    # Print environment info
    print("="*70)
    print("USD Command Line Environment Setup")
    print("="*70)
    print(f"Maya Location:  {os.environ['MAYA_LOCATION']}")
    print(f"USD Location:   {usdRootPath}")
    print(f"mayapy:         {mayapyPath}")
    print(f"USD tools:      {usdToolsPath}")
    print(f"USD libraries:  {usdLibPath}")
    print("="*70)
    print()
    print("MINIMUM PATH REQUIRED:")
    print(path_divider.join([mayapyBinPath, usdToolsPath, usdLibPath]))
    print()
    print("="*70)
    print("USAGE EXAMPLES:")
    print("="*70)
    print()
    print("# Launch UsdView:")
    print(f'  mayapy "{os.path.join(usdToolsPath, "usdview")}" "C:\\path\\to\\scene.usda"')
    print()
    print("# Inspect USD file:")
    print(f'  mayapy "{os.path.join(usdToolsPath, "usdcat")}" "C:\\path\\to\\scene.usda"')
    print()
    print("# USD tree structure:")
    print(f'  mayapy "{os.path.join(usdToolsPath, "usdtree")}" "C:\\path\\to\\scene.usda"')
    print()
    print("# Check USD file validity:")
    print(f'  mayapy "{os.path.join(usdToolsPath, "usdchecker")}" "C:\\path\\to\\scene.usda"')
    print()
    print("="*70)
    print("Opening command prompt with USD environment...")
    print("="*70)
    
    # Set up environment for the subprocess
    env = os.environ.copy()
    
    # Add USD paths to PATH
    if 'PATH' in env:
        env['PATH'] = path_divider.join([mayapyBinPath, usdToolsPath, usdLibPath, env['PATH']])
    else:
        env['PATH'] = path_divider.join([mayapyBinPath, usdToolsPath, usdLibPath])
    
    # Launch command prompt with environment
    try:
        if sys.platform in ('win32'):
            # Windows - launch cmd.exe
            subprocess.Popen(['cmd.exe'], env=env)
            print("[SUCCESS] Command prompt opened!")
            print("[INFO] The window may be behind Maya")
        else:
            # Unix - launch appropriate shell
            shell = os.environ.get('SHELL', '/bin/bash')
            subprocess.Popen([shell], env=env)
            print(f"[SUCCESS] {shell} opened!")
    except Exception as e:
        cmds.error(f'Failed to launch command shell: {e}')

# Run the function when script is executed
if __name__ == '__main__' or __name__ == 'builtins':
    setup_usdview_cmdline()

