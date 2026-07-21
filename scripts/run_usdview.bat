@echo off
cd /d C:\openusd-live-control
call scripts\env.bat || exit /b 1
if not exist scenes mkdir scenes
if not exist scenes\world.usda (
  echo #usda 1.0 > scenes\world.usda
  echo def Xform "World" { def Xform "Robot" {} def Camera "Camera" { float focalLength = 35 } } >> scenes\world.usda
)
"C:\USD\scripts\usdview_gui.bat" "%CD%\scenes\world.usda" > "%CD%\logs\viewer.log" 2>&1
