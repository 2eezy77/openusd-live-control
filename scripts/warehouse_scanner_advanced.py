"""
Advanced Warehouse Scanner - Manipulate Individual Components

This version:
1. Loads warehouse scene
2. Discovers all cameras
3. Positions a security camera to track the scanning
4. Moves boxes through warehouse
5. Changes colors based on scanning

Perfect demo of "exploding" USD and controlling parts individually!

USAGE:
1. Start Maya with bridge loaded
2. Run: python scripts/warehouse_scanner_advanced.py
"""

import subprocess
import time
import math
import json

def send(cmd):
    """Send command to Maya bridge"""
    result = subprocess.run(
        f'python scripts/send_cmd.py {cmd}', 
        shell=True, 
        capture_output=True, 
        text=True
    )
    output = result.stdout.strip()
    try:
        return json.loads(output)
    except:
        print(output)
        return {"ok": False}

def calculate_distance(pos1, pos2):
    """Calculate 3D distance between two positions"""
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def main():
    print("=" * 70)
    print("ADVANCED WAREHOUSE SCANNER - Component Control Demo")
    print("=" * 70)
    
    # ========================================================================
    # LOAD WAREHOUSE AND DISCOVER COMPONENTS
    # ========================================================================
    
    print("\n[1/6] Loading warehouse scene...")
    warehouse_path = r"C:\openusd-live-control\scenes\warehouse_with_security_cameras (3).usd"
    send(f'open "{warehouse_path}"')
    time.sleep(2)
    
    print("\n[2/6] Discovering warehouse components...")
    result = send('list_objects transform')
    
    all_objects = []
    cameras = []
    
    if result.get("ok"):
        all_objects = result.get("objects", [])
        cameras = [obj for obj in all_objects if 'camera' in obj.lower() or 'cam' in obj.lower()]
        
        print(f"   ✅ Found {len(all_objects)} total objects")
        print(f"   📹 Found {len(cameras)} security cameras")
        if cameras:
            for i, cam in enumerate(cameras[:3], 1):
                print(f"      {i}. {cam}")
    
    # ========================================================================
    # SETUP TRACKING CAMERA
    # ========================================================================
    
    print("\n[3/6] Setting up security camera tracking...")
    
    # Use first camera if found, otherwise use perspective camera
    tracking_camera = cameras[0] if cameras else "persp"
    
    if cameras:
        print(f"   📹 Using warehouse camera: {tracking_camera}")
        # Position it to watch the scanning area
        send(f'set_pose {tracking_camera} 10 12 15 -40 -20 0')
        # Highlight it in red to show it's active
        send(f'set_color {tracking_camera} red')
    else:
        print(f"   📹 Using default camera: {tracking_camera}")
        send(f'set_camera {tracking_camera} 10 12 15 -40 -20 0')
    
    # ========================================================================
    # CREATE SCANNING SYSTEM
    # ========================================================================
    
    print("\n[4/6] Creating box scanning system...")
    
    # Box types and colors
    box_types = {
        'electronics': 'blue',
        'food': 'red',
        'clothing': 'purple',
        'tools': 'orange',
        'medical': 'cyan'
    }
    
    # Incoming box type (change this!)
    incoming_type = 'electronics'
    
    # Create robot scanner
    robot_name = "Robot_Scanner"
    send(f'add_cube /World/{robot_name} 2')
    send(f'set_pose {robot_name} 0 1 0 0 0 0')
    send(f'set_color {robot_name} cyan')
    
    # Create incoming box
    box_name = f"IncomingBox_{incoming_type}"
    send(f'add_cube /World/{box_name} 2.5')
    send(f'set_pose {box_name} 15 1 0 0 0 0')
    send(f'set_color {box_name} grey')
    
    print(f"   🤖 Robot scanner created")
    print(f"   📦 Incoming box: {incoming_type}")
    print(f"   🎨 Will become: {box_types[incoming_type]}")
    
    # ========================================================================
    # SCANNING SEQUENCE
    # ========================================================================
    
    print("\n[5/6] Starting scanning sequence...")
    print("   (Security camera is recording...)")
    
    scan_distance = 3.0
    robot_start = (0, 1, 0)
    box_pos = (15, 1, 0)
    num_steps = 35
    scanned = False
    
    for step in range(num_steps + 1):
        # Move robot
        t = step / num_steps
        current_x = robot_start[0] + (box_pos[0] - robot_start[0]) * t
        current_pos = (current_x, 1, 0)
        
        send(f'set_pose {robot_name} {current_x} 1 0 0 0 0')
        
        # Calculate distance
        distance = calculate_distance(current_pos, box_pos)
        
        # Check for scan trigger
        if distance <= scan_distance and not scanned:
            print(f"\n   🎯 SCAN TRIGGERED at {distance:.2f}m")
            print(f"   📡 Scanning box...")
            
            # Highlight robot during scan
            send(f'set_color {robot_name} yellow')
            time.sleep(0.3)
            send(f'set_color {robot_name} cyan')
            
            # Change box color based on contents
            print(f"   ✅ DETECTED: {incoming_type}")
            print(f"   🎨 Applying color: {box_types[incoming_type]}")
            send(f'set_color {box_name} {box_types[incoming_type]}')
            
            # Make security camera blink (recording the event)
            if cameras:
                send(f'set_color {tracking_camera} yellow')
                time.sleep(0.2)
                send(f'set_color {tracking_camera} red')
            
            scanned = True
            print()
        
        time.sleep(0.15)
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    
    print("\n[6/6] Scanning complete!")
    
    print("\n" + "=" * 70)
    print("WAREHOUSE COMPONENT CONTROL DEMO - COMPLETE!")
    print("=" * 70)
    
    print("\n✅ What we did:")
    print("   1. Loaded complete warehouse USD file")
    print("   2. Discovered individual components (cameras, etc.)")
    print(f"   3. Controlled security camera: {tracking_camera}")
    print("   4. Created scanning robot and box")
    print("   5. Performed proximity-based color change")
    print("   6. Used camera to record the process")
    
    print("\n📦 Box Classification System:")
    for box_type, color in box_types.items():
        print(f"   • {box_type} → {color}")
    
    print("\n💡 KEY TAKEAWAY:")
    print("   You can load ANY USD file and control individual parts!")
    print("   No need to edit the USD - just discover objects and manipulate them.")
    
    print("\n" + "=" * 70)
    print("TRY DIFFERENT CONFIGURATIONS")
    print("=" * 70)
    
    print("\n1. Change box type (line 105): Try 'food', 'clothing', 'medical'")
    print("2. Position different cameras:")
    if len(cameras) > 1:
        for cam in cameras[1:3]:
            print(f"     python scripts\\send_cmd.py set_pose {cam} X Y Z RX RY RZ")
    print("3. Change warehouse floor color:")
    floors = [obj for obj in all_objects if 'floor' in obj.lower()]
    if floors:
        print(f"     python scripts\\send_cmd.py set_color {floors[0]} green")
    print("4. Hide walls to see inside:")
    walls = [obj for obj in all_objects if 'wall' in obj.lower()]
    if walls:
        print(f"     python scripts\\send_cmd.py vis {walls[0]} false")

if __name__ == "__main__":
    main()

