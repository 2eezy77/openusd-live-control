# Quick Start - OpenUSD Live Control

## Status

✅ **Phase 1 Complete**: Environment Ready  
✅ **Phase 2 Complete**: Viewer & Bridge Code Ready  
⏳ **Testing Required**: Run tests to create ready flags

## Quick Test (2 terminals)

### Terminal 1: Launch Viewer with Bridge

```batch
cd C:\openusd-live-control
scripts\run_usdview.bat
```

**What happens**:
- Creates `scenes\world.usda` (simple scene with Robot and Camera)
- Launches usdview with Hydra Storm
- Starts WebSocket bridge on 127.0.0.1:8765
- Logs to `logs\viewer.log`

**Verify**: Check logs for `[usdview-bridge] Listening on 127.0.0.1:8765`

```batch
type logs\viewer.log
```

### Terminal 2: Send Live Commands

```batch
cd C:\openusd-live-control
call scripts\env.bat
```

**Move the robot**:
```batch
python scripts\send_cmd.py set_pose /World/Robot 2 0 0 0 45 0
```
→ Robot moves to (2,0,0) with 45° rotation **instantly**!

**Hide the robot**:
```batch
python scripts\send_cmd.py toggle_visibility /World/Robot
```
→ Robot disappears/reappears

**Add a cube**:
```batch
python scripts\send_cmd.py add_prim /World/MyCube Cube
```
→ New cube appears in scene

**Move camera**:
```batch
python scripts\send_cmd.py set_camera /World/Camera 5 5 10
```
→ Camera repositions

**Remove cube**:
```batch
python scripts\send_cmd.py remove_prim /World/MyCube
```
→ Cube removed

## Manual usdview Test (Before Bridge)

Test basic usdview functionality:

```batch
C:\USD\scripts\usdview_gui.bat C:\USD\share\usd\tutorials\traversingStage\HelloWorld.usda
```

Should open viewer with a sphere.

## Architecture

```
CLI (send_cmd.py)
    ↓
WebSocket (127.0.0.1:8765)
    ↓
Bridge (usdview_bridge.py)
    ↓
USD Stage
    ↓
usdview GUI (Hydra Storm)
    → Live updates, no refresh!
```

## Files

| File | Purpose |
|------|---------|
| `scripts\run_usdview.bat` | Launch viewer with bridge |
| `scripts\send_cmd.py` | Send commands from CLI |
| `tools\usdview_bridge.py` | WebSocket server in usdview |
| `scenes\world.usda` | Auto-generated test scene |
| `logs\viewer.log` | Bridge output and errors |

## Success Flags

When testing passes, these flags will be created:

- [ ] `viewer.ready` - usdview + bridge working
- [ ] `api.ready` - All 5 commands working
- [ ] `docs.ready` - Documentation complete

## Troubleshooting

**Bridge doesn't start**:
- Check `logs\viewer.log` for Python errors
- No dependencies needed (uses standard library sockets)

**Commands fail**:
- Ensure usdview is running
- Check `logs\viewer.log` for errors

**Port in use**:
- Close other applications on port 8765
- Or edit HOST/PORT in bridge.py and send_cmd.py

## Next: Full Testing

See `TESTING.md` for comprehensive test suite.

## AMD GPU Note

This setup uses Hydra Storm, which is AMD-friendly (RX 9070 XT tested).
Check renderer menu in usdview to verify Hydra Storm is active.

