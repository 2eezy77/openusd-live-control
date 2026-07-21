# Maya USD Live Control - Start Here

**Real-time USD scene control via programmatic API**

---

## 🚀 Quick Start (2 Steps!)

### Step 1: Launch Maya
```batch
cd C:\openusd-live-control
scripts\run_maya.bat
```

### Step 2: Load Bridge in Maya

**In Maya Script Editor (Python tab) - paste this ONE line:**

```python
exec(open(r'C:\openusd-live-control\tools\maya_bridge.py').read())
```

Press **Ctrl+Enter**

**✅ You should see:**
```
[maya-bridge] Server thread started
[maya-bridge] Listening on 127.0.0.1:8765
[maya-bridge] Ready to receive commands
```

> **How to open Script Editor:** Windows → General Editors → Script Editor

---

## 🧪 Test It Works

**In terminal:**
```batch
cd C:\openusd-live-control
call scripts\env_maya.bat
python scripts\send_cmd.py list_objects
```

**✅ Expected:** `{"ok": true, ...}`

---

## 🎯 Create Your First Object

```batch
python scripts\send_cmd.py add_cube /World/Box 2
python scripts\send_cmd.py set_pose Box 0 5 0 0 0 0
python scripts\send_cmd.py set_color Box red
python scripts\send_cmd.py set_camera persp 10 10 10 -30 30 0
```

**✅ You should see a red box in Maya!**

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| **[01_COMPLETE_GUIDE.md](01_COMPLETE_GUIDE.md)** | Full documentation |
| **[02_COMMANDS.md](02_COMMANDS.md)** | All commands |
| **[03_TROUBLESHOOTING.md](03_TROUBLESHOOTING.md)** | Fix issues |
| **[04_WAREHOUSE_PROJECT.md](04_WAREHOUSE_PROJECT.md)** | Warehouse guide |
| **[05_CHARACTER_ANIMATION.md](05_CHARACTER_ANIMATION.md)** | Character guide |

---

## 🎮 Demo Scripts

```batch
# Test all features (30+ tests)
python scripts\test_complete_system.py

# Box color demo
python scripts\box_color_change.py

# Warehouse scanner
python scripts\warehouse_box_scanner.py
```

---

## 🆘 Troubleshooting

**No "Listening..." message?**
1. Check you're in **Python** tab (not MEL)
2. Make sure no spaces before `exec(`
3. Clear Script Editor (Ctrl+A, Delete) and try again

**"Connection refused"?**
- Bridge not loaded - run the exec() line again
- Check Maya Script Editor for errors

**"Object not found"?**
- Use `list_objects` to see exact names
- Names are case-sensitive

**Full troubleshooting:** [03_TROUBLESHOOTING.md](03_TROUBLESHOOTING.md)

---

## ✅ Success Checklist

- [ ] Maya opens from `run_maya.bat`
- [ ] Script Editor shows "Listening on 127.0.0.1:8765"
- [ ] `list_objects` returns JSON
- [ ] `add_cube` creates visible box
- [ ] `set_color` changes box color

**All checked?** 🎉 You're ready!

---

**The ONE line that does everything:**
```python
exec(open(r'C:\openusd-live-control\tools\maya_bridge.py').read())
```
