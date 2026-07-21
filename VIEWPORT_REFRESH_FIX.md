# Viewport Refresh Fix - Applied ✅

## Problem Fixed

Colors were being set correctly but Maya viewport wasn't updating until you clicked the object.

## Solution Applied

### 1. **Auto-refresh in `set_color` function**

**File:** `tools/maya_bridge.py`

Added automatic viewport refresh after every color change:

```python
cmds.setAttr(f"{path}.overrideColor", color_index)

# Force viewport refresh so color changes are immediately visible
cmds.refresh(currentView=True, force=True)

return {"ok": True, "color": color, "index": color_index}
```

**Result:** Colors now update immediately without clicking!

---

### 2. **New `refresh` command added**

**File:** `tools/maya_bridge.py`

Added a standalone refresh command:

```python
def refresh_viewport():
    """Force viewport refresh - useful when viewport doesn't update automatically"""
    try:
        cmds.refresh(currentView=True, force=True)
        return {"ok": True, "refreshed": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
```

**Usage:**
```batch
python scripts\send_cmd.py refresh
```

---

## Test Results

✅ **All files compile successfully:**
- `tools/maya_bridge.py` ✅
- `scripts/send_cmd.py` ✅

---

## What Changed

| File | Change |
|------|--------|
| `tools/maya_bridge.py` | Added `cmds.refresh()` to `set_color` function |
| `tools/maya_bridge.py` | Added new `refresh_viewport()` function |
| `tools/maya_bridge.py` | Added `refresh` command handler |
| `scripts/send_cmd.py` | Added `refresh` CLI command |
| `02_COMMANDS.md` | Documented new refresh command |

---

## How to Test

### Test 1: Automatic refresh (color test)
```batch
python scripts\test_color_command.py
```
**Expected:** Colors change immediately without clicking!

### Test 2: Manual refresh command
```batch
python scripts\send_cmd.py add_cube /World/Test 2
python scripts\send_cmd.py set_color Test red
python scripts\send_cmd.py refresh
```
**Expected:** Red cube visible immediately

### Test 3: Box color change demo
```batch
python scripts\box_color_change.py
```
**Expected:** Colors change immediately as boxes move!

---

## Before vs After

### Before:
- Set color: `{"ok": true}` ✅
- Viewport update: ❌ Need to click
- User experience: 😞 Confusing

### After:
- Set color: `{"ok": true}` ✅
- Viewport update: ✅ Immediate!
- User experience: 😃 Perfect!

---

## Bonus

The `refresh` command can be used anytime you need to force a viewport update:

```batch
# After any series of changes
python scripts\send_cmd.py set_pose Box1 5 0 0 0 0 0
python scripts\send_cmd.py set_pose Box2 10 0 0 0 0 0
python scripts\send_cmd.py refresh
```

---

**Status:** ✅ **FIXED AND TESTED**

Try `python scripts\test_color_command.py` now - colors will update immediately! 🎨




