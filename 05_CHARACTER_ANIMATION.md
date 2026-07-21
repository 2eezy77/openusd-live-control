# Character Kitchen Walk - Quick Start Guide

**Goal**: Make a character walk around the Pixar kitchen scene without running through objects!

---

## ✅ What's Already Done

All the commands you need are ready to use:
- ✅ `import_fbx` - Load character files
- ✅ `play` - Start animation
- ✅ `stop` - Stop animation  
- ✅ `set_time` - Jump to specific frame
- ✅ `set_pose` - Move character around
- ✅ `character_kitchen_walk.py` - Automation script

---

## 🚀 How to Get Started (3 Easy Steps)

### Step 1: Update File Paths (1 minute)

Open `scripts/character_kitchen_walk.py` and update these two lines:

```python
# Line 32 - Your character FBX path
character_fbx = r"C:\Users\Isaac\Downloads\Actorcore-Maya-1102-284522\Actor\party-m-0001\party-m-0001.fbx"

# Line 35 - Your kitchen USD path  
kitchen_usd = r"C:\Users\Isaac\Downloads\Kitchen_set\Kitchen_set\Kitchen_set.usd"
```

Make sure these paths match where you downloaded the files!

---

### Step 2: Start Maya + Bridge (30 seconds)

**Terminal 1** - Start Maya:
```batch
cd C:\openusd-live-control
scripts\run_maya.bat
```

**In Maya Script Editor** (Python tab):
```python
exec(open(r'C:\openusd-live-control\tools\maya_bridge.py').read())
```

Wait for: `[maya-bridge] Listening on 127.0.0.1:8765`

---

### Step 3: Run the Automation Script (2 minutes)

**Terminal 2**:
```batch
cd C:\openusd-live-control
call scripts\env_maya.bat

python scripts\character_kitchen_walk.py
```

**What happens**:
1. Character FBX loads into Maya
2. Kitchen USD scene loads
3. Walk animation starts playing
4. Character moves through 8 waypoints around kitchen
5. Takes about 16 seconds total (2 seconds per waypoint)

---

## 🎮 Manual Testing (Understanding the Scene)

Before running the full automation, you can test individual commands:

```batch
# Test 1: Load character manually
python scripts\send_cmd.py import_fbx "C:\Users\Isaac\Downloads\Actorcore-Maya-1102-284522\Actor\party-m-0001\party-m-0001.fbx"

# Test 2: Load kitchen manually  
python scripts\send_cmd.py open "C:\Users\Isaac\Downloads\Kitchen_set\Kitchen_set\Kitchen_set.usd"

# Test 3: Start animation
python scripts\send_cmd.py play

# Test 4: Move character (check Maya Outliner for actual name!)
python scripts\send_cmd.py set_pose party_m_0001 3 0 0 0 0 0

# Test 5: Stop animation
python scripts\send_cmd.py stop
```

---

## 🔍 Finding the Character Root Node

**IMPORTANT**: You need to know the character's root node name to move it!

**How to find it**:

1. After loading the FBX, look at **Maya Outliner** (Window → Outliner)
2. Look for the top-level object that was imported
3. Common names: `party_m_0001`, `Hips`, `Root`, `Character1`
4. Update line 38 in `character_kitchen_walk.py`:

```python
character_root = "party_m_0001"  # ← Change this to match Maya Outliner
```

**Quick test**: Try moving it with:
```batch
python scripts\send_cmd.py set_pose YOUR_ROOT_NAME_HERE 5 0 0 0 0 0
```

If it moves in Maya → correct name! ✅  
If you get "Object not found" → check Outliner again

---

## 🗺️ Refining Waypoints (Making it Look Good)

The default waypoints are just guesses. To make the character actually walk around the kitchen properly:

### Manual Method (Recommended):

1. **Load both assets** in Maya (character + kitchen)
2. **Select the character** in the viewport
3. **Use Move tool** (W key) to drag character around
4. **Find positions** that don't overlap with furniture
5. **Check Channel Box** (Ctrl+A) to see translate values
6. **Write down** 5-10 safe positions

Example safe positions you might find:
```
Kitchen entrance: (0, 0, 0)
By counter: (3, 0, 2)
Near table: (5, 0, 5)
By stove: (2, 0, 4)
Back to entrance: (0, 0, 0)
```

7. **Update waypoints** in `character_kitchen_walk.py` (line 72):

```python
waypoints = [
    (0, 0, 0, 0),      # Start at entrance
    (3, 0, 2, 90),     # Walk to counter, turn right
    (5, 0, 5, 180),    # Walk to table, turn around
    (2, 0, 4, 270),    # Walk to stove, turn left  
    (0, 0, 0, 0),      # Back to entrance
]
```

8. **Run again** - now it walks the refined path!

---

## 📋 All New Commands Reference

### Import FBX Character
```batch
python scripts\send_cmd.py import_fbx "C:\path\to\character.fbx"
```
Returns: List of imported objects

### Play Animation
```batch
# Play with current timeline range
python scripts\send_cmd.py play

# Play specific frame range (frames 1-100)
python scripts\send_cmd.py play 1 100
```

### Stop Animation
```batch
python scripts\send_cmd.py stop
```

### Jump to Frame
```batch
python scripts\send_cmd.py set_time 50
```
Jumps to frame 50

### Get Timeline Info
```batch
python scripts\send_cmd.py get_time
```
Returns: Start frame, end frame, current frame

### Move Character
```batch
python scripts\send_cmd.py set_pose CHARACTER_NAME X Y Z RX RY RZ
```
Example: `python scripts\send_cmd.py set_pose party_m_0001 5 0 0 0 90 0`

---

## 🎯 Expected Results

### When it works correctly:

1. **Maya viewport** shows:
   - Character loaded with skeleton/mesh
   - Kitchen scene with props, walls, furniture
   - Character walking animation playing
   - Character sliding through space (animation + translation)

2. **Terminal output** shows:
   ```
   [1/4] Loading character FBX...
   {"ok": true, "imported": ["party_m_0001"], ...}
   
   [2/4] Loading kitchen USD...
   {"ok": true}
   
   [3/4] Starting walk animation...
   {"ok": true, "playing": true}
   
   [4/4] Walking character through kitchen...
   → Waypoint 1/8: (0, 0, 0) @ 0°
   {"ok": true}
   ...
   ```

3. **Visual effect**: Looks like character is walking through the kitchen!

---

## 🐛 Troubleshooting

### Character doesn't load
**Error**: `"error": "Cannot load FBX"`

**Fix**: 
- Check file path is correct (use `r"C:\path\..."` with the `r` prefix)
- Check Maya has FBX plugin loaded (Window → Settings → Plug-in Manager → `fbxmaya.mll`)
- Try loading manually: File → Import → Select FBX

---

### Kitchen doesn't load
**Error**: `"error": "Cannot open file"`

**Fix**:
- Check kitchen USD path is correct
- Make sure it's the main `.usd` file (not `.usda` or `.usdc`)
- Look for `Kitchen_set.usd` in the folder

---

### Character doesn't move
**Error**: `"error": "Object not found: party_m_0001"`

**Fix**:
- Open Maya **Outliner** (Window → Outliner)
- Find the actual name of the imported character root
- Update `character_root = "..."` in the script
- Common names: `party_m_0001`, `Hips`, `mixamorig:Hips`, `Root`

---

### Character walks through walls
**Not an error** - this is expected!

**Fix**:
- Manually find safe waypoints (see "Refining Waypoints" above)
- Update the waypoints list in the script
- The default waypoints are just placeholders

---

### Animation doesn't play
**Symptom**: Character moves but legs don't animate

**Fix**:
- Check timeline is playing (press spacebar in Maya)
- Run: `python scripts\send_cmd.py play`
- Some FBX files have animation on different frame ranges
- Try: `python scripts\send_cmd.py play 0 120`

---

## 🎬 How the System Works

### The Walk Illusion

**Character has "in-place" animation**:
- Legs move in walking motion
- Character body stays at origin (like a treadmill)

**Script adds translation**:
- While legs animate in place
- `set_pose` moves the root transform through space
- Result: Looks like character is actually walking!

### Command Flow

```
Python Script
    ↓
send_cmd.py (formats command as JSON)
    ↓
Socket connection (port 8765)
    ↓
maya_bridge.py (receives JSON)
    ↓
Maya Commands (cmds.file, cmds.setAttr, cmds.play)
    ↓
Maya Viewport (updates automatically!)
```

---

## 📝 Customization Ideas

### Make it walk slower/faster
Change the `time.sleep(2)` on line 79:
```python
time.sleep(0.5)  # Faster - half second per waypoint
time.sleep(5)    # Slower - 5 seconds per waypoint
```

### Add more waypoints
Just add more positions to the waypoints list:
```python
waypoints = [
    (0, 0, 0, 0),
    (1, 0, 0, 0),
    (2, 0, 0, 0),
    (3, 0, 0, 45),   # Can even rotate mid-walk!
    # ... add as many as you want
]
```

### Make character jump
Set the Y coordinate (height):
```python
waypoints = [
    (0, 0, 0, 0),    # On ground
    (0, 2, 0, 0),    # Jump up
    (0, 0, 0, 0),    # Land
]
```

### Camera follows character
After each waypoint movement, also move camera:
```python
for i, (x, y, z, ry) in enumerate(waypoints):
    send(f'set_pose {character_root} {x} {y} {z} 0 {ry} 0')
    send(f'set_camera persp {x+5} {y+3} {z+5} -20 45 0')  # Camera behind
    time.sleep(2)
```

---

## 🎯 Success Checklist

Before you say "it works!", verify:

- [ ] Character FBX loads in Maya
- [ ] Kitchen USD loads in Maya
- [ ] Can see both in viewport at same time
- [ ] Animation plays (legs moving)
- [ ] Character moves through space when script runs
- [ ] All commands return `{"ok": true}`
- [ ] Character doesn't walk through walls (after refining waypoints)

---

## 🚀 Next Steps

Once basic walk works:

1. **Phase 1 Complete**: Assets load, character moves
2. **Phase 2**: Refine waypoints to avoid collisions
3. **Phase 3**: Add camera automation (follow character)
4. **Phase 4**: Add multiple characters (party in the kitchen!)
5. **Phase 5**: Export as video or demo for portfolio

---

## 💡 Pro Tips

### Save your Maya scene
After loading assets:
- Press **Ctrl+S** in Maya
- Saves scene with both assets
- Next time: just load saved scene instead of running script

### Check what objects exist
In Maya Script Editor (Python):
```python
import maya.cmds as cmds
cmds.ls(type='transform')  # Lists all objects
```

### Debug character name quickly
```python
# After importing FBX, run this in Maya:
import maya.cmds as cmds
print(cmds.ls(selection=True))  # Shows selected objects
```

### Record the walk as video
1. Run the script
2. In Maya: Window → Playblast
3. Exports as video file
4. Great for presentations!

---

## ❓ Questions?

Check these files:
- **README.md** - Full system documentation
- **CHEAT_SHEET.txt** - Quick command reference
- **CHARACTER_KITCHEN_PLAN.md** - Original detailed plan

Still stuck? Check:
- Maya Outliner (object names)
- Maya Script Editor (error messages)
- Terminal output (shows all command responses)

---

**Happy character walking!** 🚶‍♂️🏠✨

All commands ready - just update paths and run!



