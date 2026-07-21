"""
Discover Warehouse Components - Automatically list ALL objects

This script loads the warehouse and programmatically lists
every object you can control (cameras, walls, floor, etc.)

USAGE:
1. Start Maya with bridge loaded
2. Run: python scripts/discover_warehouse.py
"""

import subprocess
import time
import json

def send(cmd):
    """Send command to Maya bridge and return parsed JSON"""
    result = subprocess.run(
        f'python scripts/send_cmd.py {cmd}', 
        shell=True, 
        capture_output=True, 
        text=True
    )
    try:
        return json.loads(result.stdout.strip())
    except:
        print(result.stdout.strip())
        return None

def main():
    print("=" * 70)
    print("WAREHOUSE DISCOVERY - Find All Controllable Objects")
    print("=" * 70)
    
    # ========================================================================
    # LOAD WAREHOUSE
    # ========================================================================
    
    print("\n[1/3] Loading warehouse scene...")
    warehouse_path = r"C:\openusd-live-control\scenes\warehouse_with_security_cameras (3).usd"
    result = send(f'open "{warehouse_path}"')
    if result:
        print(f"   ✅ {result.get('ok', 'Loaded')}")
    
    time.sleep(2)
    
    # ========================================================================
    # DISCOVER ALL OBJECTS
    # ========================================================================
    
    print("\n[2/3] Discovering all objects in warehouse...")
    
    # Initialize variables in case discovery fails
    cameras = []
    walls = []
    floors = []
    lights = []
    others = []
    
    result = send('list_objects transform')
    
    if result and result.get("ok"):
        objects = result.get("objects", [])
        count = result.get("count", 0)
        
        print(f"   ✅ Found {count} objects!")
        
        # Categorize objects
        cameras = [obj for obj in objects if 'camera' in obj.lower() or 'cam' in obj.lower()]
        walls = [obj for obj in objects if 'wall' in obj.lower()]
        floors = [obj for obj in objects if 'floor' in obj.lower() or 'ground' in obj.lower()]
        lights = [obj for obj in objects if 'light' in obj.lower()]
        others = [obj for obj in objects if obj not in cameras + walls + floors + lights]
        
        print("\n" + "=" * 70)
        print("DISCOVERED OBJECTS - READY TO CONTROL!")
        print("=" * 70)
        
        if cameras:
            print(f"\n📹 SECURITY CAMERAS ({len(cameras)}):")
            for cam in cameras:
                print(f"   • {cam}")
            print("   Commands:")
            print(f"     python scripts\\send_cmd.py set_pose {cameras[0]} 10 15 5 -45 0 0")
            print(f"     python scripts\\send_cmd.py set_color {cameras[0]} red")
        
        if walls:
            print(f"\n🧱 WALLS ({len(walls)}):")
            for wall in walls[:5]:  # Show first 5
                print(f"   • {wall}")
            if len(walls) > 5:
                print(f"   ... and {len(walls)-5} more")
            print("   Commands:")
            print(f"     python scripts\\send_cmd.py vis {walls[0]} false  # Hide wall")
            print(f"     python scripts\\send_cmd.py set_color {walls[0]} blue")
        
        if floors:
            print(f"\n🏢 FLOORS/GROUND ({len(floors)}):")
            for floor in floors:
                print(f"   • {floor}")
            print("   Commands:")
            print(f"     python scripts\\send_cmd.py set_color {floors[0]} green")
        
        if lights:
            print(f"\n💡 LIGHTS ({len(lights)}):")
            for light in lights[:3]:
                print(f"   • {light}")
            print("   Commands:")
            print(f"     python scripts\\send_cmd.py set_pose {lights[0]} 5 10 5 -90 0 0")
        
        if others:
            print(f"\n📦 OTHER OBJECTS ({len(others)}):")
            for obj in others[:10]:  # Show first 10
                print(f"   • {obj}")
            if len(others) > 10:
                print(f"   ... and {len(others)-10} more")
    else:
        print("   ⚠️  Could not discover objects. Make sure:")
        print("      1. Maya is running")
        print("      2. Bridge is loaded (maya_bridge.py)")
        print("      3. Warehouse scene loaded successfully")
    
    # ========================================================================
    # DEMO ACTIONS
    # ========================================================================
    
    print("\n[3/3] Demo: Highlighting first camera...")
    
    if cameras:
        print(f"   Making {cameras[0]} RED...")
        send(f'set_color {cameras[0]} red')
        time.sleep(2)
        print(f"   Making {cameras[0]} CYAN...")
        send(f'set_color {cameras[0]} cyan')
    else:
        print("   ⚠️  No cameras found in scene")
        print("   Check Maya Outliner to see what objects exist")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("WAREHOUSE READY - ALL COMPONENTS ACCESSIBLE!")
    print("=" * 70)
    
    print("\n✅ You can now control individual parts!")
    print("\nCommon Actions:")
    print("  • Move cameras: set_pose CAMERA_NAME X Y Z RX RY RZ")
    print("  • Change colors: set_color OBJECT_NAME COLOR")
    print("  • Hide objects: vis OBJECT_NAME false")
    print("  • Add boxes: add_cube /World/BoxA 2")
    
    print("\n💡 NEXT: Run the warehouse scanner demo!")
    print("   python scripts\\warehouse_box_scanner.py")
    
    print("\n📝 TIP: Copy object names from above to use in your scripts!")

if __name__ == "__main__":
    main()

