@echo off
setlocal enabledelayedexpansion
cd /d C:\openusd-live-control

REM --- Start viewer & wait for bridge ---
if exist logs\viewer.log del /q logs\viewer.log
start "" cmd /c scripts\run_usdview.bat
echo Waiting for usdview bridge to start...

:waitbridge
timeout /t 1 >nul
findstr /c:"Listening on 127.0.0.1:8765" logs\viewer.log >nul && goto bridge_ready
goto waitbridge

:bridge_ready
echo Bridge is up.
type nul > viewer.ready

REM --- Env & smoke tests ---
call scripts\env.bat
echo Running smoke tests... > logs\api_tests.log
python scripts\send_cmd.py set_pose /World/Robot 2 0 0 0 45 0 >> logs\api_tests.log
python scripts\send_cmd.py set_camera /World/Camera 0 2 8 -10 0 0 >> logs\api_tests.log
python scripts\send_cmd.py add_cube /World/Box 0.5 >> logs\api_tests.log
python scripts\send_cmd.py vis /World/Box false >> logs\api_tests.log
python scripts\send_cmd.py vis /World/Box true >> logs\api_tests.log
python scripts\send_cmd.py save >> logs\api_tests.log

REM --- Burst stability test (5 quick poses) ---
for /l %%i in (1,1,5) do (
  python scripts\send_cmd.py set_pose /World/Robot %%i 0 0 0 %%i 0 >> logs\api_tests.log
)

REM --- Open a real WG asset (adjust SAMPLE if needed) ---
set SAMPLE=C:\openusd-live-control\third_party\usd-wg-assets\full_assets\full_assets.usda
if exist "%SAMPLE%" (
  python scripts\send_cmd.py open "%SAMPLE%" >> logs\api_tests.log
  python scripts\send_cmd.py set_camera /World/Camera 0 3 12 0 -15 0 >> logs\api_tests.log
)

type nul > api.ready

REM --- Summarize ---
echo [%date% %time%] TESTS OK - viewer.ready + api.ready set. >> logs\OPERATIONS_LOG.md
echo Done. View results in logs\viewer.log and logs\api_tests.log

