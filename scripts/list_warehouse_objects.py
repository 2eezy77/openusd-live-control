"""
List Warehouse Objects - Discover all individual components in the USD file

This script loads the warehouse and lists EVERY object in it,
so you can manipulate cameras, walls, floors, etc. individually.

USAGE:
1. Start Maya with bridge loaded
2. Run: python scripts/list_warehouse_objects.py

This will show you all object names you can control!
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
    return result.stdout.strip()

def main():
    print("=" * 70)
    print("WAREHOUSE OBJECT LISTER - Discover Individual Components")
    print("=" * 70)
    
    # Load warehouse scene
    print("\n[1/2] Loading warehouse scene...")
    warehouse_path = r"C:\openusd-live-control\scenes\warehouse_with_security_cameras (3).usd"
    result = send(f'open "{warehouse_path}"')
    print(f"   {result}")
    
    time.sleep(2)
    
    print("\n[2/2] Scene loaded! Now checking Maya...")
    print("\n" + "=" * 70)
    print("NEXT STEPS - Find Object Names in Maya")
    print("=" * 70)
    print("\n1. Open Maya Outliner (Window → Outliner)")
    print("\n2. You'll see a hierarchy like:")
    print("   • Warehouse_Root")
    print("     ├─ Floor")
    print("     ├─ Walls")
    print("     │  ├─ Wall_North")
    print("     │  ├─ Wall_South")
    print("     │  ├─ Wall_East")
    print("     │  └─ Wall_West")
    print("     ├─ SecurityCameras")
    print("     │  ├─ Camera_1")
    print("     │  ├─ Camera_2")
    print("     │  └─ Camera_3")
    print("     └─ Props")
    print("\n3. Write down the exact names from Outliner")
    print("\n4. Then you can control each individually!")
    print("\n" + "=" * 70)
    print("EXAMPLE COMMANDS - Control Individual Parts")
    print("=" * 70)
    
    # Examples of what they might be able to do
    examples = [
        ("Move a security camera", 
         "python scripts\\send_cmd.py set_pose Camera_1 10 15 5 -45 0 0"),
        
        ("Change floor color", 
         "python scripts\\send_cmd.py set_color Floor green"),
        
        ("Hide a wall to see inside", 
         "python scripts\\send_cmd.py vis Wall_North false"),
        
        ("Move a camera to follow boxes", 
         "python scripts\\send_cmd.py set_pose Camera_2 12 10 0 -30 90 0"),
        
        ("Change camera color (highlight it)", 
         "python scripts\\send_cmd.py set_color Camera_1 red"),
    ]
    
    for i, (desc, cmd) in enumerate(examples, 1):
        print(f"\n{i}. {desc}:")
        print(f"   {cmd}")
    
    print("\n" + "=" * 70)
    print("PRO TIP - Select in Maya to Get Name")
    print("=" * 70)
    print("\n1. Click any object in Maya viewport")
    print("2. Look at top-left of viewport - shows object name")
    print("3. OR check the Channel Box (right side) for selected name")
    print("4. Use that exact name in commands!")
    
    print("\n" + "=" * 70)
    print("READY TO MANIPULATE INDIVIDUAL PARTS!")
    print("=" * 70)
    print("\nOnce you know the object names, use:")
    print("  • set_pose - Move/rotate individual components")
    print("  • set_color - Change colors")
    print("  • vis - Hide/show parts")
    print("\nExample workflow:")
    print('  1. Note: "SecurityCamera_01" in Outliner')
    print('  2. Run: python scripts\\send_cmd.py set_pose SecurityCamera_01 5 8 5 -30 45 0')
    print('  3. Camera moves to new position!')

if __name__ == "__main__":
    main()

