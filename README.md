# Maya USD Live Control

**Real-time USD scene manipulation via programmatic API**

Control Maya and USD scenes from the command line with instant viewport updates.

---

## 📖 Documentation (Read in Order)

| File | Purpose |
|------|---------|
| **[00_START_HERE.md](00_START_HERE.md)** | Quick start guide - Begin here! |
| **[01_COMPLETE_GUIDE.md](01_COMPLETE_GUIDE.md)** | Complete system documentation |
| **[02_COMMANDS.md](02_COMMANDS.md)** | All commands reference |
| **[03_TROUBLESHOOTING.md](03_TROUBLESHOOTING.md)** | Fix common issues |
| **[04_WAREHOUSE_PROJECT.md](04_WAREHOUSE_PROJECT.md)** | Warehouse USD control |
| **[05_CHARACTER_ANIMATION.md](05_CHARACTER_ANIMATION.md)** | Character animation setup |

---

## 🚀 Quick Start

```batch
# 1. Launch Maya
cd C:\openusd-live-control
scripts\run_maya.bat

# 2. In Maya Script Editor (Python tab):
import sys
sys.path.append(r'C:\openusd-live-control\tools')
import maya_bridge

# 3. In terminal:
python scripts\send_cmd.py add_cube /World/Box 2
python scripts\send_cmd.py set_color Box red
```

**Full instructions:** [00_START_HERE.md](00_START_HERE.md)

---

## 📁 Project Structure

```
C:\openusd-live-control\
│
├── 📖 Documentation
│   ├── 00_START_HERE.md              ← Start here!
│   ├── 01_COMPLETE_GUIDE.md          ← Full documentation
│   ├── 02_COMMANDS.md                ← Command reference
│   ├── 03_TROUBLESHOOTING.md         ← Fix issues
│   ├── 04_WAREHOUSE_PROJECT.md       ← Warehouse guide
│   └── 05_CHARACTER_ANIMATION.md     ← Character guide
│
├── 🔧 Core System
│   ├── scripts/send_cmd.py           ← CLI interface
│   ├── tools/maya_bridge.py          ← Bridge (runs in Maya)
│   └── tools/load_bridge_maya.py     ← Helper loader
│
├── 🎮 Demo Scripts
│   ├── scripts/test_complete_system.py
│   ├── scripts/box_color_change.py
│   ├── scripts/warehouse_box_scanner.py
│   └── scripts/character_kitchen_walk.py
│
└── 🎬 Assets
    └── scenes/                        ← USD files
```

---

## ✨ Features

- ✅ Create and control objects programmatically
- ✅ Change colors in real-time
- ✅ Load USD files and control individual components
- ✅ Import FBX characters and control animation
- ✅ Position cameras dynamically
- ✅ Real-time viewport updates (<50ms)
- ✅ Complete Python API

---

## 🎯 Common Commands

```batch
# Create objects
python scripts\send_cmd.py add_cube /World/Box 2

# Move/rotate
python scripts\send_cmd.py set_pose Box 5 0 0 0 90 0

# Change color
python scripts\send_cmd.py set_color Box yellow

# Position camera
python scripts\send_cmd.py set_camera persp 10 10 10 -30 30 0

# List objects
python scripts\send_cmd.py list_objects
```

**Full command list:** [02_COMMANDS.md](02_COMMANDS.md)

---

## 🧪 Demo Scripts

```batch
# Test all features
python scripts\test_complete_system.py

# Box color demo
python scripts\box_color_change.py

# Warehouse scanner
python scripts\warehouse_box_scanner.py

# Character animation
python scripts\character_kitchen_walk.py
```

---

## 🆘 Need Help?

- **Getting started:** [00_START_HERE.md](00_START_HERE.md)
- **Commands not working:** [03_TROUBLESHOOTING.md](03_TROUBLESHOOTING.md)
- **Warehouse project:** [04_WAREHOUSE_PROJECT.md](04_WAREHOUSE_PROJECT.md)
- **Character animation:** [05_CHARACTER_ANIMATION.md](05_CHARACTER_ANIMATION.md)

---

## ⚡ Requirements

- Maya 2026 (Education License - Free for students)
- MayaUSD plugin (included with Maya)
- Python 3.11 (bundled with Maya)
- Windows 10/11

**Installation verified:** ✅ All systems tested and working

---

## 🎓 Learning Path

1. **Day 1:** Read [00_START_HERE.md](00_START_HERE.md) and complete quick start
2. **Day 2:** Explore [02_COMMANDS.md](02_COMMANDS.md) and run demo scripts
3. **Day 3:** Load USD files and control components
4. **Day 4+:** Build custom automation scripts

---

## ✅ Success Criteria

Your system works if:
- Maya starts from `run_maya.bat`
- Bridge shows "Listening on 127.0.0.1:8765"
- `list_objects` returns JSON
- `add_cube` creates visible box
- `set_color` changes box color
- All commands return `{"ok": true}`

**Test everything:** `python scripts\test_complete_system.py`

---

## 🎉 Ready to Start!

**Begin with:** [00_START_HERE.md](00_START_HERE.md)

You'll be controlling Maya programmatically in 5 minutes! 🚀
