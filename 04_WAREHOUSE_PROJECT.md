# Warehouse Box Scanner Project - Complete Guide

**Answer to**: "Can I load a USD file and use everything individually?"  
**Answer**: **YES!** You can "explode" any USD file and control individual components.

---

## ✅ What's Been Added

### 1. **Color Control Command** (`set_color`)
Change object colors in Maya viewport - perfect for visual feedback.

```batch
python scripts\send_cmd.py set_color OBJECT COLOR
```

**Available Colors**: red, blue, green, yellow, cyan, magenta, orange, purple, white, grey, black

### 2. **Object Discovery Command** (`list_objects`)
Programmatically discover all objects in loaded USD scenes.

```batch
# List all transforms
python scripts\send_cmd.py list_objects

# List specific types
python scripts\send_cmd.py list_objects camera
python scripts\send_cmd.py list_objects mesh
python scripts\send_cmd.py list_objects light
```

---

## 🏭 Your Warehouse Scene

**File**: `C:\openusd-live-control\scenes\warehouse_with_security_cameras (3).usd`

This USD file contains:
- 📹 Security cameras
- 🏢 Floors/ground
- 🧱 Walls
- 💡 Lights
- 📦 Other warehouse props

**All components can be controlled individually!**

---

## 🚀 Quick Start (3 Scripts to Run)

### Script 1: Discover What's Inside
```batch
cd C:\openusd-live-control
call scripts\env_maya.bat

python scripts\discover_warehouse.py
```

**What it does**:
- Loads warehouse USD
- Lists ALL objects (cameras, walls, floors, etc.)
- Shows you exact names to use in commands
- Demonstrates color control on first camera

**Output Example**:
```
📹 SECURITY CAMERAS (3):
   • Camera_01
   • Camera_02
   • Camera_03
   Commands:
     python scripts\send_cmd.py set_pose Camera_01 10 15 5 -45 0 0
     python scripts\send_cmd.py set_color Camera_01 red
```

---

### Script 2: Basic Box Scanner
```batch
python scripts\warehouse_box_scanner.py
```

**What it does**:
- Loads warehouse
- Creates robot scanner (cyan box)
- Creates incoming box (grey)
- Robot moves toward box
- When close enough (3m), box changes color based on type
  - `toys` → yellow
  - `electronics` → blue
  - `food` → red
  - `tools` → orange
  - `medical` → cyan

**Customize** (edit script line 46):
```python
incoming_box_type = 'toys'  # Change this!
```

---

### Script 3: Advanced - Control Individual Components
```batch
python scripts\warehouse_scanner_advanced.py
```

**What it does**:
- Everything from Script 2, PLUS:
- **Discovers security cameras** automatically
- **Positions specific camera** to watch scanning
- **Highlights active camera** in red
- **Makes camera blink** during scanning (yellow flash)
- Demonstrates "exploding" USD and controlling parts

**This is the key demo** - shows you can manipulate individual USD components!

---

## 💡 Manual Control Examples

After loading warehouse, you can manually control any discovered object:

### Move Security Camera
```batch
# Get object names first
python scripts\send_cmd.py list_objects

# Move specific camera
python scripts\send_cmd.py set_pose Camera_01 10 15 5 -45 30 0
```

### Change Colors
```batch
# Highlight camera in red
python scripts\send_cmd.py set_color Camera_01 red

# Change floor color
python scripts\send_cmd.py set_color Floor_01 green

# Make walls blue
python scripts\send_cmd.py set_color Wall_North blue
```

### Hide/Show Objects
```batch
# Hide wall to see inside
python scripts\send_cmd.py vis Wall_North false

# Show it again
python scripts\send_cmd.py vis Wall_North true
```

### Add New Boxes
```batch
# Create box in warehouse
python scripts\send_cmd.py add_cube /World/BoxA 2

# Position it
python scripts\send_cmd.py set_pose BoxA 8 1 5 0 0 0

# Color it
python scripts\send_cmd.py set_color BoxA yellow
```

---

## 🎯 The "Explode and Use Individually" Workflow

### Step 1: Load Any USD File
```batch
python scripts\send_cmd.py open "C:\path\to\any_scene.usd"
```

### Step 2: Discover What's Inside
```batch
python scripts\send_cmd.py list_objects
```

Returns JSON with all object names:
```json
{
  "ok": true,
  "objects": ["Camera_01", "Floor", "Wall_North", ...],
  "count": 47,
  "type": "transform"
}
```

### Step 3: Control Individual Parts
```batch
# Now you know the names, control them!
python scripts\send_cmd.py set_pose Camera_01 X Y Z RX RY RZ
python scripts\send_cmd.py set_color Wall_North blue
python scripts\send_cmd.py vis Floor false
```

**No USD editing needed!** Just load and manipulate.

---

## 📋 Complete Command Reference

### Color Control
```batch
python scripts\send_cmd.py set_color OBJECT COLOR

# Examples
python scripts\send_cmd.py set_color Camera_01 red
python scripts\send_cmd.py set_color BoxA yellow
python scripts\send_cmd.py set_color Floor green
```

### Object Discovery
```batch
# List all transforms (objects you can move)
python scripts\send_cmd.py list_objects

# List all cameras
python scripts\send_cmd.py list_objects camera

# List all meshes
python scripts\send_cmd.py list_objects mesh

# List everything
python scripts\send_cmd.py list_objects all
```

### Position Control (existing)
```batch
python scripts\send_cmd.py set_pose OBJECT X Y Z RX RY RZ
```

### Visibility Control (existing)
```batch
python scripts\send_cmd.py vis OBJECT true|false
```

### Camera Control (existing)
```batch
python scripts\send_cmd.py set_camera CAMERA X Y Z RX RY RZ
```

---

## 🎬 Demo Scenarios

### Scenario 1: Security Camera Following Robot
```python
# In your script:
# 1. Discover cameras
cameras = list_objects("camera")

# 2. Position camera to watch scanning area
set_pose(cameras[0], 10, 12, 15, -40, -20, 0)

# 3. Highlight it
set_color(cameras[0], "red")

# 4. Move robot through scene
# 5. Camera "watches" the action!
```

### Scenario 2: Color-Coded Warehouse Zones
```python
# Different zones different colors
set_color("Floor_Zone_A", "green")   # Receiving
set_color("Floor_Zone_B", "blue")    # Sorting
set_color("Floor_Zone_C", "yellow")  # Shipping

# Boxes change color as they move through zones!
```

### Scenario 3: Hide Walls for X-Ray View
```python
# Hide walls to see inside
set_visibility("Wall_North", False)
set_visibility("Wall_West", False)

# Now you can see robot working inside!
```

---

## 🔧 Customization Options

### Box Types and Colors
Edit in script (line ~45):
```python
box_classifications = {
    'toys': 'yellow',
    'electronics': 'blue',
    'books': 'green',
    'tools': 'orange',
    'food': 'red',
    'clothing': 'purple',
    'medical': 'cyan'
}
```

Add your own categories!

### Scanning Distance
```python
scan_distance = 3.0  # Distance in Maya units
```

### Robot Speed
```python
num_steps = 40  # More steps = slower movement
time.sleep(0.2)  # Pause between steps
```

### Camera Positions
```python
# Position camera wherever you want
send(f'set_camera persp 20 15 20 -35 45 0')
```

---

## 📊 What Makes This Work?

### USD Hierarchy
```
warehouse_with_security_cameras.usd
├─ /World
│  ├─ Floor_01
│  ├─ Walls
│  │  ├─ Wall_North
│  │  ├─ Wall_South
│  │  └─ ...
│  ├─ SecurityCameras
│  │  ├─ Camera_01
│  │  ├─ Camera_02
│  │  └─ Camera_03
│  └─ Lights
```

### Our System
1. **Loads USD** → All prims become Maya objects
2. **Discovers objects** → `list_objects` queries Maya scene
3. **Controls individually** → `set_pose`, `set_color`, `vis` work on any object
4. **Real-time updates** → Maya viewport updates instantly

**Key insight**: Once loaded, USD prims are just Maya objects - you can manipulate them like anything else!

---

## 🎯 Why This is Powerful

### For Your Project
✅ **Realistic**: Warehouse with actual cameras and structure  
✅ **Automated**: Robot scans boxes and changes colors  
✅ **Visual**: Color coding shows box classification  
✅ **Professional**: Security cameras "recording" the process

### General Use
✅ **Any USD file**: Load any scene, discover components  
✅ **No editing**: Don't need to modify USD files  
✅ **Programmatic**: Script everything  
✅ **Real-time**: See changes instantly in Maya

---

## 🐛 Troubleshooting

### "Object not found"
**Solution**: Run `discover_warehouse.py` first to get exact names.

### "No cameras found"
**Solution**: Check Maya Outliner - cameras might have different names.

### Objects don't move
**Solution**: Some USD objects might be locked. Try:
```python
# In Maya Script Editor
import maya.cmds as cmds
cmds.setAttr("ObjectName.translateX", lock=False)
```

### Can't see color changes
**Solution**: Make sure Maya is in **Shaded mode** (Press **6** in viewport).

---

## 📚 Files Created

| File | Purpose |
|------|---------|
| `scripts/box_color_change.py` | Basic box color demo (no warehouse) |
| `scripts/test_color_command.py` | Test color command |
| `scripts/warehouse_box_scanner.py` | Basic warehouse scanner |
| `scripts/warehouse_scanner_advanced.py` | Advanced with camera control |
| `scripts/discover_warehouse.py` | Discover all warehouse components |
| `scripts/list_warehouse_objects.py` | Manual discovery guide |
| `WAREHOUSE_PROJECT_GUIDE.md` | This file! |

---

## 🎓 Key Takeaways

### Question: "Can I load part of a USD file and use everything individually?"

### Answer: **YES!**

**How**:
1. Load complete USD file (`open` command)
2. Discover components (`list_objects` command)
3. Control individually (`set_pose`, `set_color`, `vis` on specific names)

**No USD editing needed** - just load and manipulate!

### This Works For:
- ✅ Warehouse scenes
- ✅ Character rigs (move individual joints)
- ✅ Complex assemblies (control each part)
- ✅ Any hierarchical USD file

---

## 🚀 Next Steps

1. **Run discovery script**:
   ```batch
   python scripts\discover_warehouse.py
   ```

2. **Note object names** from output

3. **Run advanced scanner**:
   ```batch
   python scripts\warehouse_scanner_advanced.py
   ```

4. **Experiment**! Try:
   - Moving different cameras
   - Changing box types
   - Positioning boxes on warehouse shelves
   - Creating multiple scanning stations

5. **Build your own** scenarios using the components!

---

**Your warehouse USD file is perfect for this demo!** 🏭📹🤖

All the scripts are ready to run - just start Maya with the bridge and go!

