@echo off
REM Maya USD Live Control - Launch Maya with Bridge
REM This script:
REM 1. Sets up Maya environment
REM 2. Launches Maya with command port enabled on 8765
REM 3. Loads the USD scene automatically

cd /d C:\openusd-live-control

REM Setup environment
call scripts\env_maya.bat
if %ERRORLEVEL% NEQ 0 (
    echo Failed to setup Maya environment
    pause
    exit /b 1
)

REM Create scenes directory if needed
if not exist scenes mkdir scenes

REM Check if world.usda exists, create if needed
if not exist scenes\world.usda (
    echo Creating default USD scene...
    (
        echo #usda 1.0
        echo ^(
        echo     defaultPrim = "World"
        echo ^)
        echo.
        echo def Xform "World"
        echo {
        echo     def Xform "Robot"
        echo     {
        echo         double3 xformOp:translate = ^(0, 0, 0^)
        echo         double3 xformOp:rotateXYZ = ^(0, 0, 0^)
        echo         uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ"]
        echo     }
        echo.
        echo     def Camera "Camera"
        echo     {
        echo         double3 xformOp:translate = ^(0, 5, 10^)
        echo         double3 xformOp:rotateXYZ = ^(-20, 0, 0^)
        echo         uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ"]
        echo         float focalLength = 35
        echo     }
        echo }
    ) > scenes\world.usda
    echo Created scenes\world.usda
)

echo.
echo ============================================
echo Maya USD Live Control
echo ============================================
echo Maya Version: %MAYA_VERSION%
echo Maya Location: %MAYA_LOCATION%
echo Command Port: 8765
echo ============================================
echo.
echo IMPORTANT: After Maya launches:
echo 1. Create some objects (cube, sphere, etc.)
echo 2. In Script Editor (Python tab), run:
echo    exec(open(r'%CD%\tools\maya_bridge.py').read())
echo.
echo Then from another terminal:
echo    python scripts\send_cmd.py set_pose pCube1 2 0 0 0 45 0
echo.
echo ============================================
echo Launching Maya with new scene...
echo ============================================
echo.

REM Launch Maya with fresh scene (no file loading)
"%MAYA_LOCATION%\bin\maya.exe"

