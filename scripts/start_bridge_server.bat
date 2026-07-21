@echo off
echo.
echo ================================================================
echo   STANDALONE BRIDGE SERVER  
echo ================================================================
echo.
echo Starting bridge server on 127.0.0.1:8765...
echo Once running, you can:
echo   1. Open usdview manually: C:\USD\scripts\usdview.bat scenes\world.usda
echo   2. Use send_cmd.py to control the scene
echo.

cd /d C:\openusd-live-control

REM Set USD environment
set USD_ROOT=C:\USD
set PATH=%USD_ROOT%\bin;%USD_ROOT%\lib;%PATH%
set PYTHONPATH=%USD_ROOT%\lib\python;%PYTHONPATH%
set PXR_PLUGINPATH_NAME=%USD_ROOT%\plugin

C:\USD\python\python.exe tools\bridge_standalone.py

