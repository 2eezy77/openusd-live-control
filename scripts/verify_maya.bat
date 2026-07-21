@echo off
REM Verification script for Maya and MayaUSD installation
REM Run this after installing Maya to verify everything is set up correctly

echo ============================================
echo Maya USD Installation Verification
echo ============================================
echo.

REM Check for Maya installations (2023, 2024, 2025, 2026)
set MAYA_FOUND=0
set MAYA_VERSION=

if exist "C:\Program Files\Autodesk\Maya2026\bin\maya.exe" (
    set MAYA_VERSION=2026
    set MAYA_FOUND=1
    set MAYA_LOCATION=C:\Program Files\Autodesk\Maya2026
)
if exist "C:\Program Files\Autodesk\Maya2025\bin\maya.exe" (
    set MAYA_VERSION=2025
    set MAYA_FOUND=1
    set MAYA_LOCATION=C:\Program Files\Autodesk\Maya2025
)
if exist "C:\Program Files\Autodesk\Maya2024\bin\maya.exe" (
    set MAYA_VERSION=2024
    set MAYA_FOUND=1
    set MAYA_LOCATION=C:\Program Files\Autodesk\Maya2024
)
if exist "C:\Program Files\Autodesk\Maya2023\bin\maya.exe" (
    set MAYA_VERSION=2023
    set MAYA_FOUND=1
    set MAYA_LOCATION=C:\Program Files\Autodesk\Maya2023
)

if %MAYA_FOUND%==0 (
    echo [FAIL] Maya not found!
    echo.
    echo Please install Maya 2023, 2024, 2025, or 2026 from:
    echo https://www.autodesk.com/education/home
    echo.
    pause
    exit /b 1
)

echo [OK] Found Maya %MAYA_VERSION%
echo     Location: %MAYA_LOCATION%
echo.

REM Check maya.exe
if exist "%MAYA_LOCATION%\bin\maya.exe" (
    echo [OK] maya.exe found
) else (
    echo [FAIL] maya.exe not found
)

REM Check mayapy.exe
if exist "%MAYA_LOCATION%\bin\mayapy.exe" (
    echo [OK] mayapy.exe found
) else (
    echo [FAIL] mayapy.exe not found
)

REM Check for MayaUSD .mod file
if exist "C:\Program Files\Common Files\Autodesk Shared\Modules\Maya\mayaUSD.mod" (
    echo [OK] MayaUSD.mod file found
) else (
    echo [WARN] MayaUSD.mod file not found (may be OK if bundled with Maya)
)

REM Check for MayaUSD installation directory
set MAYAUSD_FOUND=0
if exist "C:\Program Files\Autodesk\MayaUSD" (
    echo [OK] MayaUSD installation directory found
    set MAYAUSD_FOUND=1
)

echo.
echo ============================================
echo Testing mayapy Python environment...
echo ============================================
echo.

REM Test pxr module import
"%MAYA_LOCATION%\bin\mayapy.exe" -c "from pxr import Usd; print('[OK] USD Python module (pxr) imports successfully')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] Could not import pxr module - MayaUSD may not be loaded yet
    echo       Launch Maya and enable mayaUsdPlugin.mll in Plug-in Manager
)

echo.
echo ============================================
echo Environment Summary
echo ============================================
echo Maya Version: %MAYA_VERSION%
echo Maya Location: %MAYA_LOCATION%
if %MAYAUSD_FOUND%==1 (
    echo MayaUSD: Installed
) else (
    echo MayaUSD: Bundled with Maya (check Plug-in Manager)
)
echo.
echo Next Steps:
echo 1. Launch Maya
echo 2. Go to: Windows ^> Settings/Preferences ^> Plug-in Manager
echo 3. Enable mayaUsdPlugin.mll (check Loaded + Auto Load)
echo 4. Run this script again to verify pxr module
echo.
pause

