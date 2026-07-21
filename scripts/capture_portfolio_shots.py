"""
Capture portfolio screenshots of a demo Maya / USD Live Control scene.
Run inside Maya (GUI):

  exec(open(r'C:/Users/Isaac/work/1-projects/openusd-live-control/scripts/capture_portfolio_shots.py').read())
"""
from __future__ import annotations

import os
from pathlib import Path

import maya.cmds as cmds

ROOT = Path(r"C:\Users\Isaac\work\1-projects\openusd-live-control")
OUT = ROOT / "docs"
OUT.mkdir(parents=True, exist_ok=True)


def _assign_color(shape: str, rgb: tuple[float, float, float], name: str) -> None:
    shader = cmds.shadingNode("lambert", asShader=True, name=f"{name}_SG_mat")
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{name}_SG")
    cmds.connectAttr(f"{shader}.outColor", f"{sg}.surfaceShader", force=True)
    cmds.setAttr(f"{shader}.color", rgb[0], rgb[1], rgb[2], type="double3")
    cmds.sets(shape, edit=True, forceElement=sg)


def build_scene() -> None:
    cmds.file(new=True, force=True)
    # Ground plane
    ground = cmds.polyPlane(name="Ground", w=20, h=20, sx=1, sy=1)[0]
    _assign_color(cmds.listRelatives(ground, shapes=True)[0], (0.18, 0.20, 0.24), "Ground")

    boxes = [
        ("Box_Red", (-3, 1, 0), (0.85, 0.18, 0.18)),
        ("Box_Blue", (0, 1, 0), (0.20, 0.45, 0.95)),
        ("Box_Yellow", (3, 1, 0), (0.95, 0.80, 0.15)),
    ]
    for name, t, rgb in boxes:
        cube = cmds.polyCube(name=name, w=2, h=2, d=2)[0]
        cmds.move(t[0], t[1], t[2], cube)
        _assign_color(cmds.listRelatives(cube, shapes=True)[0], rgb, name)

    # Camera framing like a live-control demo
    if not cmds.objExists("persp"):
        cmds.camera(name="persp")
    cmds.setAttr("persp.translate", 8.5, 6.5, 10.5, type="double3")
    cmds.setAttr("persp.rotate", -28, 40, 0, type="double3")
    cmds.lookThru("persp")

    # Soft grey backdrop
    cmds.setAttr("defaultRenderGlobals.imageFormat", 32)  # png
    try:
        cmds.displayPref(displayGradient=True)
    except Exception:
        pass


def playblast(path: Path, w: int = 1600, h: int = 900) -> Path:
    # Maya appends frame number; normalize afterward
    stem = str(path.with_suffix(""))
    cmds.playblast(
        filename=stem,
        format="image",
        compression="png",
        quality=100,
        viewer=False,
        showOrnaments=False,
        forceOverwrite=True,
        percent=100,
        widthHeight=[w, h],
        frame=[1],
        clearCache=True,
        offScreen=True,
    )
    # Find produced frame file
    candidates = list(path.parent.glob(path.stem + "*.png"))
    if not candidates:
        raise RuntimeError(f"Playblast produced no PNG near {path}")
    produced = max(candidates, key=lambda p: p.stat().st_mtime)
    final = path if path.suffix.lower() == ".png" else path.with_suffix(".png")
    if produced.resolve() != final.resolve():
        if final.exists():
            final.unlink()
        produced.replace(final)
    return final


def main() -> None:
    build_scene()
    shot1 = playblast(OUT / "maya-viewport-live.png")
    # Second angle after a "live" transform (simulates send_cmd set_pose / set_color)
    cmds.move(1, 0, 0, "Box_Red", relative=True)
    cmds.rotate(0, 35, 0, "Box_Blue", relative=True)
    # Recolor yellow -> green as if set_color ran
    mats = cmds.ls("Box_Yellow_SG_mat", type="lambert") or []
    if mats:
        cmds.setAttr(f"{mats[0]}.color", 0.20, 0.75, 0.35, type="double3")
    cmds.setAttr("persp.translate", 7.5, 5.5, 9.0, type="double3")
    cmds.setAttr("persp.rotate", -24, 48, 0, type="double3")
    shot2 = playblast(OUT / "maya-viewport-commands.png")
    print(f"[capture] wrote {shot1}")
    print(f"[capture] wrote {shot2}")
    # Marker for the launcher
    (OUT / ".capture_done").write_text("ok\n", encoding="utf-8")


main()
