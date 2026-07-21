# NVIDIA USD Limitation & Solutions

## Issue

NVIDIA's prebuilt USD does NOT support the `--python` flag in usdview, which our bridge relies on.

**Error**:
```
usdview: error: unrecognized arguments: --python tools\usdview_bridge.py
```

## Solutions

### Option 1: Build Standard OpenUSD (Recommended for Full Features)

Build OpenUSD from source with Python support:

```powershell
# Download and extract OpenUSD source
cd C:\Downloads
git clone https://github.com/PixarAnimationStudios/OpenUSD.git
cd OpenUSD

# Build (1-2 hours)
python build_scripts/build_usd.py --python C:\USD-custom

# Replace C:\USD
cd C:\openusd-live-control
scripts\cleanup_windows.ps1  # Archives current C:\USD
Move-Item C:\USD-custom C:\USD
```

Then our scripts will work as designed with `--python` flag.

### Option 2: Use USD Python Interpreter Console (Manual Workflow)

**Steps**:

1. **Start usdview normally**:
   ```batch
   C:\USD\scripts\usdview.bat C:\openusd-live-control\scenes\world.usda
   ```

2. **Open Python Interpreter** in usdview:
   - Menu: Window → Interpreter
   - OR press ` (backtick key)

3. **Paste bridge code** into interpreter:
   ```python
   import json, socket, threading
   from pxr import UsdGeom, Gf
   
   def handle_cmd(cmd):
       stage = appController._dataModel.stage
       if cmd["cmd"] == "set_pose":
           path = cmd["path"]
           t, r = cmd["t"], cmd["r"]
           xf = UsdGeom.Xformable(stage.GetPrimAtPath(path))
           for op in xf.GetOrderedXformOps(): xf.RemoveXformOp(op)
           xf.AddTranslateOp().Set(Gf.Vec3d(*t))
           xf.AddRotateXYZOp().Set(Gf.Vec3d(*r))
           appController._dataModel.stage.Reload()
       return {"ok": True}
   
   def serve():
       s = socket.socket()
       s.bind(("127.0.0.1", 8765))
       s.listen(1)
       print("[bridge] Listening on 127.0.0.1:8765")
       while True:
           conn, _ = s.accept()
           res = handle_cmd(json.loads(conn.recv(65536).decode()))
           conn.sendall(json.dumps(res).encode())
           conn.close()
   
   threading.Thread(target=serve, daemon=True).start()
   ```

4. **Send commands** from separate terminal:
   ```batch
   cd C:\openusd-live-control
   python scripts\send_cmd.py set_pose /World/Robot 2 0 0 0 45 0
   ```

### Option 3: Use usd-core from PyPI (No usdview GUI)

Simpler but no visualization:

```powershell
cd C:\openusd-live-control
.\.venv\Scripts\activate
pip install usd-core
python scripts\send_cmd.py set_pose /World/Robot 2 0 0 0 45 0
# Scene modified, but no viewer to see it
```

### Option 4: File-Based Communication (Workaround)

Modify bridge to watch a command file instead of socket:

```python
# Bridge watches commands.json
# Updates USD file  
# usdview auto-reloads on file change
```

This avoids plugin loading entirely.

## Recommendation

For this project's goals (live visual control with usdview):

**Best**: Build standard OpenUSD from source (Option 1)
- Supports --python flag
- Full features
- Our code works as-is

**Quickest**: Use Python interpreter console (Option 2)
- Works with NVIDIA build
- Manual setup each time
- Good for testing

## Current Status

- ❌ `--python` flag doesn't work with NVIDIA prebuilt
- ⚠️ Project blocked until standard USD build obtained
- ✅ All code is correct, just needs compatible USD

## Updated Instructions

See logs/OPERATIONS_LOG.md for detailed decision on which option to pursue.

