"""
Box Color Change Demo - Proximity-based color changing

BoxA moves toward BoxB. When they get close, BoxB changes color
based on BoxA's name (toys=yellow, cars=blue, etc.)

USAGE:
1. Start Maya with bridge loaded
2. Run: python scripts/box_color_change.py
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
    print("BOX COLOR CHANGE - Proximity Detection Demo")
    print("=" * 70)
    
    # ========================================================================
    # CONFIGURATION
    # ========================================================================
    
    # Box names and their associated colors
    box_types = {
        'toys': 'yellow',
        'cars': 'blue',
        'books': 'green',
        'tools': 'orange',
        'food': 'red'
    }
    
    # Choose what type BoxA is (change this to test different colors!)
    box_a_type = 'toys'  # Try: 'toys', 'cars', 'books', 'tools', 'food'
    
    # Starting position for BoxA
    start_pos = (0, 1, 0)
    
    # Target position (where BoxB is waiting)
    target_pos = (10, 1, 0)
    
    # Distance threshold for "meeting" (when to change color)
    meeting_distance = 2.0
    
    # ========================================================================
    # SETUP SCENE
    # ========================================================================
    
    print("\n[1/4] Creating boxes...")
    
    # Create BoxA (the moving box)
    box_a_name = f"BoxA_{box_a_type}"
    send(f'add_cube /World/{box_a_name} 2')
    send(f'set_pose {box_a_name} {start_pos[0]} {start_pos[1]} {start_pos[2]} 0 0 0')
    send(f'set_color {box_a_name} cyan')  # Start color for BoxA
    
    time.sleep(0.5)
    
    # Create BoxB (the waiting box that will change color)
    box_b_name = "BoxB"
    send(f'add_cube /World/{box_b_name} 2')
    send(f'set_pose {box_b_name} {target_pos[0]} {target_pos[1]} {target_pos[2]} 0 0 0')
    send(f'set_color {box_b_name} grey')  # Start as grey (neutral)
    
    print(f"\n   BoxA type: {box_a_type} (will trigger {box_types[box_a_type]} color)")
    print(f"   BoxA position: {start_pos}")
    print(f"   BoxB position: {target_pos}")
    
    # ========================================================================
    # SETUP CAMERA
    # ========================================================================
    
    print("\n[2/4] Setting up camera view...")
    
    # Position camera to see both boxes
    mid_x = (start_pos[0] + target_pos[0]) / 2
    send(f'set_camera persp {mid_x} 8 15 -30 0 0')
    
    # ========================================================================
    # MOVE BoxA TOWARD BoxB
    # ========================================================================
    
    print("\n[3/4] Moving BoxA toward BoxB...")
    print(f"   Watching for distance < {meeting_distance} units\n")
    
    # Calculate movement steps
    num_steps = 30
    color_changed = False
    
    for step in range(num_steps + 1):
        # Interpolate position from start to target
        t = step / num_steps  # 0.0 to 1.0
        current_x = start_pos[0] + (target_pos[0] - start_pos[0]) * t
        current_y = start_pos[1]
        current_z = start_pos[2]
        
        current_pos = (current_x, current_y, current_z)
        
        # Move BoxA
        send(f'set_pose {box_a_name} {current_x} {current_y} {current_z} 0 0 0')
        
        # Calculate distance between boxes
        distance = calculate_distance(current_pos, target_pos)
        
        print(f"   Step {step+1}/{num_steps+1}: BoxA at ({current_x:.1f}, {current_y:.1f}, {current_z:.1f}) - Distance: {distance:.2f}")
        
        # Check if boxes are close enough
        if distance <= meeting_distance and not color_changed:
            print(f"\n   🎯 BOXES MEET! Distance: {distance:.2f} <= {meeting_distance}")
            print(f"   🎨 Changing BoxB color to {box_types[box_a_type]} (because BoxA is '{box_a_type}')")
            
            # Change BoxB's color based on BoxA's type!
            send(f'set_color {box_b_name} {box_types[box_a_type]}')
            color_changed = True
            time.sleep(1)  # Pause to appreciate the color change
            print()
        
        time.sleep(0.3)  # Smooth animation
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    
    print("\n[4/4] Demo complete!")
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ BoxA (type: '{box_a_type}') moved from {start_pos} to {target_pos}")
    print(f"✅ When boxes got within {meeting_distance} units, BoxB changed to {box_types[box_a_type]}")
    print("\nTry changing 'box_a_type' on line 52 to:")
    for box_type, color in box_types.items():
        print(f"  - '{box_type}' → BoxB becomes {color}")
    print("\nYou can also adjust:")
    print("  - meeting_distance (line 60) - how close they need to be")
    print("  - start_pos/target_pos (lines 54-57) - where boxes are")
    print("  - num_steps (line 108) - speed of movement")

if __name__ == "__main__":
    main()

