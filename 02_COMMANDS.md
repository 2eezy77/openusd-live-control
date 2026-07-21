# Command Reference

Complete reference for all Maya USD Live Control commands.

---

## 📋 Basic Commands

### Create Cube
```batch
python scripts\send_cmd.py add_cube /World/NAME SIZE
```
**Example:** `python scripts\send_cmd.py add_cube /World/Box1 2`

---

### Move/Rotate Object
```batch
python scripts\send_cmd.py set_pose NAME X Y Z RX RY RZ
```
- `X Y Z` = Position coordinates
- `RX RY RZ` = Rotation in degrees

**Example:** `python scripts\send_cmd.py set_pose Box1 5 0 0 0 90 0`

---

### Change Color
```batch
python scripts\send_cmd.py set_color NAME COLOR
```

**Available Colors:**
`red`, `blue`, `green`, `yellow`, `cyan`, `magenta`, `orange`, `purple`, `white`, `grey`, `black`, `brown`

**Example:** `python scripts\send_cmd.py set_color Box1 yellow`

---

### Position Camera
```batch
python scripts\send_cmd.py set_camera CAMERA X Y Z RX RY RZ
```
**Example:** `python scripts\send_cmd.py set_camera persp 10 10 10 -30 45 0`

---

### Hide/Show Object
```batch
python scripts\send_cmd.py vis NAME true|false
```
**Examples:**
```batch
python scripts\send_cmd.py vis Box1 false  # Hide
python scripts\send_cmd.py vis Box1 true   # Show
```

---

### Delete Object
```batch
python scripts\send_cmd.py rm NAME
```
**Example:** `python scripts\send_cmd.py rm Box1`

---

### List All Objects
```batch
python scripts\send_cmd.py list_objects
```
Returns JSON with all scene objects.

---

### Refresh Viewport
```batch
python scripts\send_cmd.py refresh
```
Forces Maya viewport to refresh. Useful if changes aren't visible immediately.

**Note:** Color changes now auto-refresh, so you rarely need this!

---

### Load USD File
```batch
python scripts\send_cmd.py open "C:\path\to\file.usd"
```
**Example:** `python scripts\send_cmd.py open "C:\scenes\warehouse.usd"`

---

## 🎬 Animation Commands

### Import FBX Character
```batch
python scripts\send_cmd.py import_fbx "C:\path\to\character.fbx"
```

---

### Play Animation
```batch
python scripts\send_cmd.py play
python scripts\send_cmd.py play START_FRAME END_FRAME
```
**Examples:**
```batch
python scripts\send_cmd.py play              # Play current range
python scripts\send_cmd.py play 1 100        # Play frames 1-100
```

---

### Stop Animation
```batch
python scripts\send_cmd.py stop
```

---

### Set Frame
```batch
python scripts\send_cmd.py set_time FRAME
```
**Example:** `python scripts\send_cmd.py set_time 50`

---

### Get Timeline Info
```batch
python scripts\send_cmd.py get_time
```
Returns start frame, end frame, and current frame.

---

## 📐 Common Patterns

### Create & Position Box
```batch
python scripts\send_cmd.py add_cube /World/Robot 2
python scripts\send_cmd.py set_pose Robot 0 1 0 0 0 0
python scripts\send_cmd.py set_color Robot cyan
```

---

### Create Scene Layout
```batch
# Floor
python scripts\send_cmd.py add_cube /World/Floor 20
python scripts\send_cmd.py set_pose Floor 0 -0.5 0 0 0 0
python scripts\send_cmd.py set_color Floor grey

# Box
python scripts\send_cmd.py add_cube /World/Box 2
python scripts\send_cmd.py set_pose Box 0 1 0 0 0 0
python scripts\send_cmd.py set_color Box red

# Camera
python scripts\send_cmd.py set_camera persp 10 10 10 -30 30 0
```

---

### Standard Camera Positions
```batch
# Wide shot
python scripts\send_cmd.py set_camera persp 15 10 15 -30 30 0

# Medium shot
python scripts\send_cmd.py set_camera persp 8 5 8 -25 30 0

# Close shot
python scripts\send_cmd.py set_camera persp 3 2 3 -15 45 0

# Top view
python scripts\send_cmd.py set_camera persp 0 20 0 -90 0 0

# Side view
python scripts\send_cmd.py set_camera persp 15 0 0 0 90 0
```

---

## 🧪 Test Commands

### Complete System Test
```batch
python scripts\test_complete_system.py
```
Tests all 30+ commands automatically.

---

### Test Color Command
```batch
python scripts\test_color_command.py
```
Cycles through all available colors.

---

### Test Animation Commands
```batch
python scripts\test_animation_commands.py
```
Tests play, stop, set_time, get_time.

---

## 📊 Command Return Values

**Success:**
```json
{"ok": true, ...additional data...}
```

**Failure:**
```json
{"ok": false, "error": "Error message"}
```

---

## 🎯 Tips

1. **Object names are case-sensitive** - Check Maya Outliner for exact names
2. **Use `list_objects`** - Always check what exists in scene
3. **Position camera first** - So you can see your objects
4. **Colors only show in viewport** - Press `6` for hardware texturing mode
5. **Test with simple commands** - Start with `list_objects` to verify connection

---

**Need help?** See [03_TROUBLESHOOTING.md](03_TROUBLESHOOTING.md)

