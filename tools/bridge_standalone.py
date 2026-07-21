"""
Standalone USD Bridge Server
Monitors scenes/world.usda and applies commands via file modification
"""
import json, socket, threading, time
from pathlib import Path
from pxr import Usd, UsdGeom, Sdf, Gf

PORT = 8765
SCENE_PATH = "scenes/world.usda"

print("[bridge-standalone] Starting USD bridge server...")
print(f"[bridge-standalone] Scene: {SCENE_PATH}")

stage = Usd.Stage.Open(SCENE_PATH)
if not stage:
    print(f"[bridge-standalone] ERROR: Could not open {SCENE_PATH}")
    exit(1)

print(f"[bridge-standalone] Stage loaded: {stage.GetRootLayer().identifier}")

def _ensure_xform(stage, path):
    prim = stage.GetPrimAtPath(path)
    if not prim: prim = UsdGeom.Xform.Define(stage, path).GetPrim()
    return UsdGeom.Xformable(prim)

def set_pose(stage, path, t=(0,0,0), r=(0,0,0), s=(1,1,1)):
    xf = _ensure_xform(stage, path)
    for op in xf.GetOrderedXformOps(): xf.RemoveXformOp(op)
    xf.AddScaleOp().Set(Gf.Vec3d(*s))
    rx, ry, rz = [Gf.DegreesToRadians(v) for v in r]
    xf.AddRotateZOp().Set(rz*180/3.141592653589793)
    xf.AddRotateYOp().Set(ry*180/3.141592653589793)
    xf.AddRotateXOp().Set(rx*180/3.141592653589793)
    xf.AddTranslateOp().Set(Gf.Vec3d(*t))
    stage.Save()  # Save to trigger usdview reload

def set_visibility(stage, path, visible=True):
    p = stage.GetPrimAtPath(path)
    if p and p.IsValid():
        img = UsdGeom.Imageable(p)
        img.MakeVisible() if visible else img.MakeInvisible()
        stage.Save()

def add_cube(stage, path, size=1.0):
    UsdGeom.Cube.Define(stage, path).CreateSizeAttr(size)
    stage.Save()

def remove_prim(stage, path): 
    if stage.GetPrimAtPath(path):
        stage.RemovePrim(path)
        stage.Save()

def set_attr(stage, path, attr, value):
    prim = stage.GetPrimAtPath(path)
    if prim:
        a = prim.GetAttribute(attr) or prim.CreateAttribute(attr, Sdf.ValueTypeNames.Token)
        a.Set(value)
        stage.Save()

def set_camera(stage, cam="/World/Camera", t=(0,0,10), r=(0,0,0)):
    cam_prim = UsdGeom.Camera.Define(stage, cam)
    xf = UsdGeom.Xformable(cam_prim.GetPrim())
    for op in xf.GetOrderedXformOps(): xf.RemoveXformOp(op)
    rx, ry, rz = [Gf.DegreesToRadians(v) for v in r]
    xf.AddRotateZOp().Set(rz*180/3.141592653589793)
    xf.AddRotateYOp().Set(ry*180/3.141592653589793)
    xf.AddRotateXOp().Set(rx*180/3.141592653589793)
    xf.AddTranslateOp().Set(Gf.Vec3d(*t))
    stage.Save()

def handle(cmd):
    global stage
    c = cmd.get("cmd")
    try:
        if c == "set_pose":
            set_pose(stage, cmd.get("path","/World/Robot"),
                     tuple(cmd.get("t",(0,0,0))), tuple(cmd.get("r",(0,0,0))), tuple(cmd.get("s",(1,1,1))))
        elif c == "set_visibility": set_visibility(stage, cmd["path"], bool(cmd.get("visible", True)))
        elif c == "add_cube":       add_cube(stage, cmd["path"], float(cmd.get("size",1.0)))
        elif c == "remove_prim":    remove_prim(stage, cmd["path"])
        elif c == "set_attr":       set_attr(stage, cmd["path"], cmd["attr"], cmd["value"])
        elif c == "set_camera":     set_camera(stage, cmd.get("path","/World/Camera"),
                                               tuple(cmd.get("t",(0,0,10))), tuple(cmd.get("r",(0,0,0))))
        elif c == "reload":
            stage = Usd.Stage.Open(SCENE_PATH)
            return {"ok": True, "msg": "Stage reloaded"}
        elif c == "save":
            stage.Save()
        else:
            return {"ok": False, "error": f"unknown cmd {c}"}
        return {"ok": True}
    except Exception as e:
        import traceback
        return {"ok": False, "error": str(e), "trace": traceback.format_exc()}

def serve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", PORT))
    s.listen(1)
    print(f"[bridge-standalone] Listening on 127.0.0.1:{PORT}")
    print("[bridge-standalone] Ready for commands!")
    print("[bridge-standalone] Open usdview: C:\\USD\\scripts\\usdview.bat scenes\\world.usda")
    print("")
    
    while True:
        conn, addr = s.accept()
        try:
            data = conn.recv(65536).decode("utf-8")
            cmd = json.loads(data)
            print(f"[bridge-standalone] Command: {cmd.get('cmd')} on {cmd.get('path', 'N/A')}")
            res = handle(cmd)
            conn.sendall(json.dumps(res).encode("utf-8"))
            if res.get("ok"):
                print(f"[bridge-standalone] ✓ Success")
            else:
                print(f"[bridge-standalone] ✗ Error: {res.get('error')}")
        except Exception as e:
            print(f"[bridge-standalone] Exception: {e}")
            conn.sendall(json.dumps({"ok":False,"error":str(e)}).encode("utf-8"))
        finally:
            conn.close()

if __name__ == "__main__":
    serve()

