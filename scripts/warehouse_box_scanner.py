"""
Warehouse Box Scanner - Robot sorting boxes by type

Scenario: A warehouse robot (BoxA) scans incoming boxes (BoxB).
When the robot gets close enough, it "scans" the box and changes its 
color based on what's inside (toys=yellow, cars=blue, etc.)

Perfect for warehouse with security cameras scene!

USAGE:
1. Start Maya with bridge loaded
2. Run: python scripts/warehouse_box_scanner.py
"""

import subprocess
import time
import math

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

def calculate_distance(pos1, pos2):
    """Calculate 3D distance between two positions"""
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def main():
    print("=" * 70)
    print("WAREHOUSE BOX SCANNER - Automated Sorting System")
    print("=" * 70)
    
    # ========================================================================
    # CONFIGURATION
    # ========================================================================
    
    # Box types and their color codes (what robot "scans")
    box_classifications = {
        'toys': 'yellow',
        'electronics': 'blue',
        'books': 'green',
        'tools': 'orange',
        'food': 'red',
        'clothing': 'purple',
        'medical': 'cyan'
    }
    
    # What's in the incoming box? (change this to test different items!)
    incoming_box_type = 'toys'  # Try: toys, electronics, books, tools, food, clothing, medical
    
    # Robot scanner position (on conveyor belt entrance)
    robot_start = (0, 1, 0)
    
    # Box waiting position (on conveyor belt)
    box_position = (15, 1, 0)
    
    # Scanning distance (how close robot needs to get)
    scan_distance = 3.0
    
    # ========================================================================
    # LOAD WAREHOUSE SCENE
    # ========================================================================
    
    print("\n[1/5] Loading warehouse scene...")
    warehouse_path = r"C:\openusd-live-control\scenes\warehouse_with_security_cameras (3).usd"
    send(f'open "{warehouse_path}"')
    
    time.sleep(2)
    print("   ✅ Warehouse loaded (with security cameras monitoring!)")
    
    # ========================================================================
    # CREATE ROBOT SCANNER
    # ========================================================================
    
    print("\n[2/5] Creating robot scanner...")
    
    robot_name = "RobotScanner"
    send(f'add_cube /World/{robot_name} 2')
    send(f'set_pose {robot_name} {robot_start[0]} {robot_start[1]} {robot_start[2]} 0 0 0')
    send(f'set_color {robot_name} cyan')  # Robot is cyan (scanning laser color)
    
    print(f"   ✅ Robot scanner created at {robot_start}")
    
    # ========================================================================
    # CREATE INCOMING BOX
    # ========================================================================
    
    print("\n[3/5] Creating incoming box...")
    
    box_name = f"Box_{incoming_box_type}"
    send(f'add_cube /World/{box_name} 2.5')  # Slightly bigger than robot
    send(f'set_pose {box_name} {box_position[0]} {box_position[1]} {box_position[2]} 0 0 0')
    send(f'set_color {box_name} grey')  # Unscanned boxes are grey
    
    print(f"   ✅ Incoming box created at {box_position}")
    print(f"   📦 Contents: {incoming_box_type}")
    print(f"   🎨 Will become: {box_classifications[incoming_box_type]}")
    
    # ========================================================================
    # SETUP WAREHOUSE CAMERA VIEW
    # ========================================================================
    
    print("\n[4/5] Setting up security camera view...")
    
    # Position camera above warehouse floor to see the action
    mid_x = (robot_start[0] + box_position[0]) / 2
    send(f'set_camera persp {mid_x} 12 20 -35 0 0')
    
    print("   ✅ Security camera view positioned")
    
    # ========================================================================
    # ROBOT SCANNING SEQUENCE
    # ========================================================================
    
    print("\n[5/5] Robot scanning sequence starting...")
    print(f"   🤖 Robot moving from {robot_start} toward box at {box_position}")
    print(f"   📡 Scan will activate at distance < {scan_distance} units\n")
    
    num_steps = 40
    scanned = False
    
    for step in range(num_steps + 1):
        # Move robot toward box
        t = step / num_steps
        current_x = robot_start[0] + (box_position[0] - robot_start[0]) * t
        current_y = robot_start[1]
        current_z = robot_start[2]
        
        current_pos = (current_x, current_y, current_z)
        
        # Move robot
        send(f'set_pose {robot_name} {current_x} {current_y} {current_z} 0 0 0')
        
        # Calculate distance to box
        distance = calculate_distance(current_pos, box_position)
        
        # Print status
        status = "⚪" if distance > scan_distance else "🔴"
        print(f"   {status} Step {step+1}/{num_steps+1}: Distance to box: {distance:.2f}m", end="")
        
        # Check if in scanning range
        if distance <= scan_distance and not scanned:
            print("\n")
            print(f"   🎯 SCAN ACTIVATED! Robot within {scan_distance}m")
            print(f"   📡 Scanning box contents...")
            time.sleep(0.5)
            print(f"   ✅ DETECTED: {incoming_box_type.upper()}")
            print(f"   🎨 Applying color code: {box_classifications[incoming_box_type].upper()}")
            
            # Change box color based on what robot "scanned"
            send(f'set_color {box_name} {box_classifications[incoming_box_type]}')
            
            # Flash robot to show scanning
            send(f'set_color {robot_name} yellow')
            time.sleep(0.3)
            send(f'set_color {robot_name} cyan')
            
            scanned = True
            print()
        else:
            print()
        
        time.sleep(0.2)
    
    # ========================================================================
    # SUMMARY REPORT
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("WAREHOUSE SORTING COMPLETE")
    print("=" * 70)
    print(f"\n📦 Scanned Item: {incoming_box_type}")
    print(f"🎨 Color Code: {box_classifications[incoming_box_type]}")
    print(f"✅ Box sorted and ready for warehouse storage")
    print(f"📹 Security cameras recorded the entire process")
    
    print("\n" + "-" * 70)
    print("TRY DIFFERENT BOX TYPES")
    print("-" * 70)
    print("\nChange line 46 (incoming_box_type) to:")
    for item_type, color in box_classifications.items():
        print(f"  • '{item_type}' → {color} box")
    
    print("\n" + "-" * 70)
    print("CUSTOMIZATION OPTIONS")
    print("-" * 70)
    print("\n  • scan_distance (line 52) - scanning range")
    print("  • robot_start (line 49) - where robot begins")
    print("  • box_position (line 52) - where boxes arrive")
    print("  • num_steps (line 94) - robot movement speed")
    
    print("\n" + "-" * 70)
    print("WAREHOUSE FEATURES")
    print("-" * 70)
    print("\n  ✅ Security cameras monitoring")
    print("  ✅ Automated box scanning")
    print("  ✅ Color-coded sorting system")
    print("  ✅ Real-time distance detection")
    
    print("\n💡 Tip: Check Maya Outliner to see warehouse structure!")
    print("   You can position boxes on shelves, in aisles, etc.")

if __name__ == "__main__":
    main()

