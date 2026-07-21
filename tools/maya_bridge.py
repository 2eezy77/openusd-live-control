"""
Maya USD Live Control Bridge
Socket server that translates JSON commands to maya.cmds calls for real-time USD scene manipulation

This script runs INSIDE Maya and listens on port 8765 for commands from send_cmd.py
Commands are translated to Maya commands that manipulate USD prims through MayaUSD

USAGE IN MAYA:
1. Load a USD file in Maya
2. Run this script in Maya Script Editor (Python tab)
3. Bridge starts listening on 127.0.0.1:8765
4. Send commands from terminal: python scripts/send_cmd.py set_pose /World/Robot 2 0 0 0 45 0

OR use commandPort (automatic):
Launch Maya with: maya -command "commandPort -name ':8765'"
"""

import json
import socket
import threading
import traceback

import maya.cmds as cmds
import maya.api.OpenMaya as om

PORT = 8765
_server_thread = None
_server_running = False

def get_usd_prim_path(maya_path):
    """
    Convert Maya DAG path to USD prim path
    If it's already a USD path (starts with /), return as-is
    Otherwise, try to find the USD prim path for the Maya object
    """
    if maya_path.startswith('/'):
        return maya_path
    
    # For Maya objects, we need to get their USD proxy path
    # This is simplified - in practice, you'd query the USD stage
    return maya_path

def set_pose(path, t=(0, 0, 0), r=(0, 0, 0), s=(1, 1, 1)):
    """
    Set position, rotation, and scale of a USD prim or Maya object
    t: translate (x, y, z)
    r: rotate (rx, ry, rz) in degrees
    s: scale (sx, sy, sz)
    """
    # Check if object exists
    if not cmds.objExists(path):
        # Try to create a transform node
        if '/' in path:
            # USD path - create using mayaUsd commands
            return {"ok": False, "error": f"USD prim not found: {path}"}
        else:
            # Create Maya transform
            path = cmds.createNode('transform', name=path.split('/')[-1])
    
    # Set transform attributes
    try:
        cmds.setAttr(f"{path}.translateX", t[0])
        cmds.setAttr(f"{path}.translateY", t[1])
        cmds.setAttr(f"{path}.translateZ", t[2])
        
        cmds.setAttr(f"{path}.rotateX", r[0])
        cmds.setAttr(f"{path}.rotateY", r[1])
        cmds.setAttr(f"{path}.rotateZ", r[2])
        
        cmds.setAttr(f"{path}.scaleX", s[0])
        cmds.setAttr(f"{path}.scaleY", s[1])
        cmds.setAttr(f"{path}.scaleZ", s[2])
        
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def set_visibility(path, visible=True):
    """Toggle visibility of an object"""
    if not cmds.objExists(path):
        return {"ok": False, "error": f"Object not found: {path}"}
    
    try:
        cmds.setAttr(f"{path}.visibility", 1 if visible else 0)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def set_color(path, color):
    """
    Set display color of an object (Maya viewport override color)
    color can be: 'red', 'blue', 'green', 'yellow', 'cyan', 'magenta', 'white', 'black'
    or a number 0-31 (Maya color index)
    """
    if not cmds.objExists(path):
        return {"ok": False, "error": f"Object not found: {path}"}
    
    # Color name to Maya index mapping
    color_map = {
        'black': 1,
        'grey': 2,
        'light_grey': 3,
        'red': 13,
        'blue': 6,
        'green': 14,
        'yellow': 17,
        'cyan': 18,
        'magenta': 9,
        'brown': 10,
        'orange': 20,
        'purple': 30,
        'white': 16
    }
    
    try:
        # Enable color override
        cmds.setAttr(f"{path}.overrideEnabled", 1)
        cmds.setAttr(f"{path}.overrideRGBColors", 0)  # Use index colors
        
        # Set color
        if isinstance(color, str):
            color_index = color_map.get(color.lower(), 13)  # Default to red
        else:
            color_index = int(color)
        
        cmds.setAttr(f"{path}.overrideColor", color_index)
        
        # Force viewport refresh so color changes are immediately visible
        cmds.refresh(currentView=True, force=True)
        
        return {"ok": True, "color": color, "index": color_index}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def refresh_viewport():
    """Force viewport refresh - useful when viewport doesn't update automatically"""
    try:
        cmds.refresh(currentView=True, force=True)
        return {"ok": True, "refreshed": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def add_cube(path, size=1.0):
    """Create a cube primitive"""
    try:
        # Get the name from path
        name = path.split('/')[-1]
        
        # Create cube
        cube = cmds.polyCube(name=name, width=size, height=size, depth=size)[0]
        
        # If path has parent hierarchy, try to parent it
        if '/' in path:
            parent_path = '/'.join(path.split('/')[:-1])
            if parent_path and cmds.objExists(parent_path):
                cmds.parent(cube, parent_path)
        
        return {"ok": True, "created": cube}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def remove_prim(path):
    """Delete an object"""
    if not cmds.objExists(path):
        return {"ok": False, "error": f"Object not found: {path}"}
    
    try:
        cmds.delete(path)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def set_attr(path, attr, value):
    """Set custom attribute on an object"""
    if not cmds.objExists(path):
        return {"ok": False, "error": f"Object not found: {path}"}
    
    try:
        attr_full = f"{path}.{attr}"
        
        # Check if attribute exists
        if not cmds.attributeQuery(attr, node=path, exists=True):
            # Create attribute
            cmds.addAttr(path, longName=attr, dataType='string')
        
        # Set attribute value
        cmds.setAttr(attr_full, value, type='string')
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def set_camera(cam="/World/Camera", t=(0, 0, 10), r=(0, 0, 0)):
    """Set camera position and rotation"""
    # Find or create camera
    if not cmds.objExists(cam):
        # Create camera
        cam_name = cam.split('/')[-1]
        cam = cmds.camera(name=cam_name)[0]
    
    try:
        # Set camera transform
        cmds.setAttr(f"{cam}.translateX", t[0])
        cmds.setAttr(f"{cam}.translateY", t[1])
        cmds.setAttr(f"{cam}.translateZ", t[2])
        
        cmds.setAttr(f"{cam}.rotateX", r[0])
        cmds.setAttr(f"{cam}.rotateY", r[1])
        cmds.setAttr(f"{cam}.rotateZ", r[2])
        
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def open_stage(path):
    """Open a USD file in Maya"""
    try:
        # Import USD file
        cmds.file(path, open=True, force=True)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def save(filepath=None):
    """
    Save the current Maya scene
    Uses production-tested pattern: rename + save with force=True
    Based on: https://forums.autodesk.com/t5/maya-programming/save-as/
    """
    try:
        import os
        
        # Check if scene has been saved before
        current_file = cmds.file(query=True, sceneName=True)
        
        if not current_file or current_file == "":
            # Scene is untitled - use Maya's default project location
            if not filepath:
                # Get Maya's current workspace (default project)
                workspace = cmds.workspace(query=True, rootDirectory=True)
                scenes_dir = os.path.join(workspace, "scenes")
                
                # Ensure scenes directory exists
                if not os.path.exists(scenes_dir):
                    os.makedirs(scenes_dir)
                
                filepath = os.path.join(scenes_dir, "maya_scene.ma")
            
            # Production-tested "Save As" pattern
            # Step 1: Rename the scene in Maya's internal memory
            cmds.file(rename=filepath)
            
            # Step 2: Save with force=True (prevents prompts)
            cmds.file(save=True, force=True, type="mayaAscii")
            
            return {
                "ok": True, 
                "saved": filepath, 
                "message": "Saved as new file (Maya default location)"
            }
        else:
            # Scene already has a filename - simple save
            cmds.file(save=True, force=True)
            return {
                "ok": True, 
                "saved": current_file, 
                "message": "Saved existing file"
            }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ============================================================================
# ANIMATION COMMANDS - CHARACTER KITCHEN PROJECT
# DELETE FROM HERE TO "END ANIMATION COMMANDS" TO REMOVE THIS FEATURE
# ============================================================================

def play_animation(start=None, end=None):
    """
    Play animation timeline
    
    Args:
        start: Optional start frame
        end: Optional end frame
    
    Returns:
        {"ok": true, "playing": true} or error
    """
    try:
        # Set timeline range if provided
        if start is not None and end is not None:
            cmds.playbackOptions(minTime=start, maxTime=end)
        
        # Start playback
        cmds.play(forward=True)
        
        return {"ok": True, "playing": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def stop_animation():
    """
    Stop animation playback
    
    Returns:
        {"ok": true, "playing": false} or error
    """
    try:
        cmds.play(state=False)
        return {"ok": True, "playing": False}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def set_time(frame):
    """
    Set current timeline frame
    
    Args:
        frame: Frame number to jump to
    
    Returns:
        {"ok": true, "frame": current_frame} or error
    """
    try:
        cmds.currentTime(frame)
        current = cmds.currentTime(query=True)
        return {"ok": True, "frame": current}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def get_animation_range():
    """
    Get animation timeline information
    
    Returns:
        {"ok": true, "start": min_frame, "end": max_frame, "current": current_frame} or error
    """
    try:
        start = cmds.playbackOptions(query=True, minTime=True)
        end = cmds.playbackOptions(query=True, maxTime=True)
        current = cmds.currentTime(query=True)
        
        return {
            "ok": True, 
            "start": start, 
            "end": end, 
            "current": current
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def import_fbx(filepath):
    """
    Import FBX file into Maya scene
    
    Args:
        filepath: Path to FBX file
    
    Returns:
        {"ok": true, "imported": [list of imported objects]} or error
    """
    try:
        # Import FBX file
        # Using i=True means "import" (merge into current scene)
        # type="FBX" tells Maya it's an FBX file
        # ignoreVersion=True prevents version warnings
        # mergeNamespacesOnClash=False keeps original names
        cmds.file(filepath, i=True, type="FBX", ignoreVersion=True, mergeNamespacesOnClash=False)
        
        # Get what was just imported (Maya selects newly imported objects)
        imported = cmds.ls(selection=True)
        
        # If nothing selected, get all transform nodes (less precise but works)
        if not imported:
            imported = ["Check Maya Outliner for imported objects"]
        
        return {
            "ok": True, 
            "imported": imported,
            "message": f"Imported {len(imported)} object(s)"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def list_objects(object_type="transform"):
    """
    List all objects in the scene
    
    Args:
        object_type: Type of objects to list (default: "transform")
                    Options: "transform", "mesh", "camera", "light", "all"
    
    Returns:
        {"ok": true, "objects": [...], "count": N} or error
    """
    try:
        if object_type == "all":
            # Get all nodes
            objects = cmds.ls()
        else:
            # Get specific type
            objects = cmds.ls(type=object_type)
        
        # Filter out default Maya objects that users don't care about
        filtered = [obj for obj in objects if not obj.startswith('default') 
                    and not obj.startswith('initial')
                    and not obj.startswith('render')
                    and not obj.startswith('global')
                    and not obj.startswith('hardwareRenderingGlobals')
                    and not obj.startswith('ikSystem')]
        
        return {
            "ok": True,
            "objects": filtered,
            "count": len(filtered),
            "type": object_type
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ============================================================================
# END ANIMATION COMMANDS
# ============================================================================

def handle_command(cmd):
    """
    Handle incoming JSON command and execute appropriate Maya operation
    """
    c = cmd.get("cmd")
    
    try:
        if c == "set_pose":
            return set_pose(
                cmd.get("path", "/World/Robot"),
                tuple(cmd.get("t", (0, 0, 0))),
                tuple(cmd.get("r", (0, 0, 0))),
                tuple(cmd.get("s", (1, 1, 1)))
            )
        
        elif c == "set_visibility":
            return set_visibility(
                cmd["path"],
                bool(cmd.get("visible", True))
            )
        
        elif c == "set_color":
            return set_color(
                cmd["path"],
                cmd.get("color", "red")
            )
        
        elif c == "add_cube":
            return add_cube(
                cmd["path"],
                float(cmd.get("size", 1.0))
            )
        
        elif c == "remove_prim":
            return remove_prim(cmd["path"])
        
        elif c == "set_attr":
            return set_attr(
                cmd["path"],
                cmd["attr"],
                cmd["value"]
            )
        
        elif c == "set_camera":
            return set_camera(
                cmd.get("path", "/World/Camera"),
                tuple(cmd.get("t", (0, 0, 10))),
                tuple(cmd.get("r", (0, 0, 0)))
            )
        
        elif c == "open_stage":
            return open_stage(cmd["path"])
        
        elif c == "save":
            return save()
        
        # Animation commands
        elif c == "play":
            return play_animation(
                cmd.get("start"),
                cmd.get("end")
            )
        
        elif c == "stop":
            return stop_animation()
        
        elif c == "set_time":
            return set_time(cmd["frame"])
        
        elif c == "get_time":
            return get_animation_range()
        
        elif c == "import_fbx":
            return import_fbx(cmd["path"])
            
        elif c == "set_color":
            return set_color(
                cmd["path"],
                cmd.get("color", "red")
            )
        
        elif c == "list_objects":
            return list_objects(cmd.get("type", "transform"))
        
        elif c == "refresh":
            return refresh_viewport()
        
        else:
            return {"ok": False, "error": f"Unknown command: {c}"}

    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "trace": traceback.format_exc()
        }

def serve():
    """
    Socket server that listens for commands on port 8765
    Runs in background thread to not block Maya UI
    """
    global _server_running
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind(("127.0.0.1", PORT))
        s.listen(1)
        _server_running = True
        print(f"[maya-bridge] Listening on 127.0.0.1:{PORT}")
        print("[maya-bridge] Ready to receive commands from send_cmd.py")
        
        while _server_running:
            s.settimeout(1.0)  # Allow checking _server_running flag
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue
            
            try:
                # Receive command
                data = conn.recv(65536)
                if not data:
                    conn.close()
                    continue
                
                # Parse JSON
                cmd = json.loads(data.decode("utf-8"))
                print(f"[maya-bridge] Received command: {cmd.get('cmd')} {cmd.get('path', '')}")
                
                # Execute command
                result = handle_command(cmd)
                
                # Send response
                conn.sendall(json.dumps(result).encode("utf-8"))
                
                if result.get("ok"):
                    print(f"[maya-bridge] Command successful")
                else:
                    print(f"[maya-bridge] Command failed: {result.get('error')}")
                
            except Exception as e:
                error_result = {
                    "ok": False,
                    "error": str(e),
                    "trace": traceback.format_exc()
                }
                try:
                    conn.sendall(json.dumps(error_result).encode("utf-8"))
                except:
                    pass
                print(f"[maya-bridge] Error: {e}")
            
            finally:
                conn.close()
    
    except Exception as e:
        print(f"[maya-bridge] Server error: {e}")
    finally:
        s.close()
        _server_running = False
        print("[maya-bridge] Server stopped")

def start_server():
    """Start the bridge server in a background thread"""
    global _server_thread, _server_running
    
    if _server_running:
        print("[maya-bridge] Server already running!")
        return
    
    _server_thread = threading.Thread(target=serve, daemon=True)
    _server_thread.start()
    print("[maya-bridge] Server thread started")

def stop_server():
    """Stop the bridge server"""
    global _server_running
    _server_running = False
    print("[maya-bridge] Stopping server...")

# Auto-start when script is loaded in Maya
# This triggers whether imported or exec()'d
start_server()

