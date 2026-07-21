@echo off
REM Maya USD Live Control - Environment Setup
REM Sets up paths for Maya, MayaUSD, and USD tools

REM Auto-detect Maya installation (check 2026, 2025, 2024, 2023)
set MAYA_FOUND=0

if exist "C:\Program Files\Autodesk\Maya2026\bin\maya.exe" (
    set MAYA_LOCATION=C:\Program Files\Autodesk\Maya2026
    set MAYA_VERSION=2026
    set MAYA_FOUND=1
)

if %MAYA_FOUND%==0 if exist "C:\Program Files\Autodesk\Maya2025\bin\maya.exe" (
    set MAYA_LOCATION=C:\Program Files\Autodesk\Maya2025
    set MAYA_VERSION=2025
    set MAYA_FOUND=1
)

if %MAYA_FOUND%==0 if exist "C:\Program Files\Autodesk\Maya2024\bin\maya.exe" (
    set MAYA_LOCATION=C:\Program Files\Autodesk\Maya2024
    set MAYA_VERSION=2024
    set MAYA_FOUND=1
)

if %MAYA_FOUND%==0 if exist "C:\Program Files\Autodesk\Maya2023\bin\maya.exe" (
    set MAYA_LOCATION=C:\Program Files\Autodesk\Maya2023
    set MAYA_VERSION=2023
    set MAYA_FOUND=1
)

if %MAYA_FOUND%==0 (
    echo ERROR: Maya not found!
    echo Please install Maya 2023, 2024, 2025, or 2026 from:
    echo https://www.autodesk.com/education/home
    exit /b 1
)

echo Found Maya %MAYA_VERSION% at %MAYA_LOCATION%

REM Set Maya paths
set PATH=%MAYA_LOCATION%\bin;%PATH%

REM MayaUSD should set USD_LOCATION when plugin loads
REM But we can set a fallback if needed
if exist "C:\Program Files\Autodesk\MayaUSD\Maya%MAYA_VERSION%" (
    REM MayaUSD is installed separately
    set MAYAUSD_LOCATION=C:\Program Files\Autodesk\MayaUSD\Maya%MAYA_VERSION%
    echo Found MayaUSD at %MAYAUSD_LOCATION%
)

REM Python from Maya
set PYTHONPATH=%MAYA_LOCATION%\Python;%MAYA_LOCATION%\Python\Lib\site-packages;%PYTHONPATH%

echo Environment configured for Maya %MAYA_VERSION%
echo Ready to launch Maya or run mayapy scripts

