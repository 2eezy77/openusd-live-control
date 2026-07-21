@echo off
REM Note: Do NOT use setlocal - we need these vars to persist for calling scripts
set USD_ROOT=C:\USD

REM NVIDIA prebuilt USD comes with bundled Python environment
REM Set up paths to use the bundled USD Python
set PATH=%USD_ROOT%\bin;%USD_ROOT%\lib;%PATH%
set PYTHONPATH=%USD_ROOT%\lib\python;%PYTHONPATH%
set PXR_PLUGINPATH_NAME=%CD%\plugins;%USD_ROOT%\plugin

REM Create venv if needed (prefer Python 3.12 to match USD)
if not exist .venv ( py -3.12 -m venv .venv 2>nul || py -3.11 -m venv .venv 2>nul || py -3.10 -m venv .venv )

REM Use the bundled Python from USD
set PYTHON_EXE=%USD_ROOT%\python\python.exe

REM Test pxr module import
%PYTHON_EXE% -c "from pxr import Usd, UsdGeom; print('pxr ok')" > logs\env.txt 2>&1

