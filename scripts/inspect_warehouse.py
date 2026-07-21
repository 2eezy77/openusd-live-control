"""
Inspect Warehouse Scene - View contents of the warehouse USD file

This script loads the warehouse scene and prints out all the objects in it,
so we can see what's available (security cameras, floor, walls, etc.)

USAGE:
1. Start Maya with bridge loaded
2. Run: python scripts/inspect_warehouse.py
"""

import subprocess
import time

def send(cmd):
    """Send command to Maya bridge"""
    result = subprocess.run(
        f'python scripts/send_cmd.py {cmd}', 
        shell=True, 
        capture_output=True, 
        text=True
    )
    print(result.stdout.strip())
    return result.stdout

def main():
    print("=" * 70)
    print("WAREHOUSE SCENE INSPECTOR")
    print("=" * 70)
    
    warehouse_path = r"C:\openusd-live-control\scenes\warehouse_with_security_cameras (3).usd"
    
    print(f"\n[1/2] Loading warehouse scene...")
    print(f"   Path: {warehouse_path}")
    send(f'open "{warehouse_path}"')
    
    time.sleep(2)
    
    print("\n[2/2] Scene loaded!")
    print("\n" + "=" * 70)
    print("Next Steps:")
    print("=" * 70)
    print("\n1. Check Maya Outliner (Window → Outliner) to see all objects")
    print("2. Look for:")
    print("   - Floor/ground objects")
    print("   - Security camera objects")
    print("   - Walls or boundaries")
    print("   - Any existing boxes or props")
    print("\n3. Note down object names from the Outliner")
    print("\n4. You can position boxes in the warehouse by using:")
    print("   python scripts\\send_cmd.py add_cube /World/BoxA 2")
    print("   python scripts\\send_cmd.py set_pose BoxA X Y Z 0 0 0")
    print("\n5. Set camera to view the warehouse:")
    print("   python scripts\\send_cmd.py set_camera persp 20 15 20 -30 45 0")
    print("\nThe box color change demo will work great in this warehouse!")
    print("Just adjust the positions in box_color_change.py to fit the space.")

if __name__ == "__main__":
    main()

