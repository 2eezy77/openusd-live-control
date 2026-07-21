"""
Test Color Command - Quick verification that set_color works

This script tests the new set_color command by creating a cube
and cycling through all available colors.

USAGE:
1. Start Maya with bridge loaded
2. Run: python scripts/test_color_command.py
"""

import subprocess
import time

def send(cmd):
    """Send command and display result"""
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
    print("COLOR COMMAND TEST - Quick Verification")
    print("=" * 70)
    
    # ========================================================================
    # CREATE TEST CUBE
    # ========================================================================
    
    print("\n[1/3] Creating test cube...")
    send('add_cube /World/ColorTest 3')
    send('set_pose ColorTest 0 2 0 0 0 0')
    
    # Position camera
    print("\n[2/3] Setting up camera...")
    send('set_camera persp 8 5 8 -20 30 0')
    
    time.sleep(1)
    
    # ========================================================================
    # TEST ALL COLORS
    # ========================================================================
    
    print("\n[3/3] Testing all colors...\n")
    
    colors = [
        'red', 'blue', 'green', 'yellow', 
        'cyan', 'magenta', 'orange', 'purple',
        'white', 'grey', 'brown', 'black'
    ]
    
    print(f"Will cycle through {len(colors)} colors:")
    for i, color in enumerate(colors):
        print(f"  {i+1}. {color}")
    
    print("\nStarting color cycle...\n")
    
    for i, color in enumerate(colors):
        print(f"[{i+1}/{len(colors)}] Setting to {color.upper()}...")
        send(f'set_color ColorTest {color}')
        time.sleep(1)  # Pause so you can see each color
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("COLOR TEST COMPLETE!")
    print("=" * 70)
    print("\n✅ If the cube changed colors in Maya viewport, set_color works!")
    print("\nAvailable colors:")
    print("  - Basic: red, blue, green, yellow")
    print("  - Extended: cyan, magenta, orange, purple")
    print("  - Neutral: white, grey, brown, black")
    print("\nUsage:")
    print('  python scripts\\send_cmd.py set_color OBJECT COLOR')
    print('  Example: python scripts\\send_cmd.py set_color pCube1 yellow')
    print("\nReady to run the full demo:")
    print('  python scripts\\box_color_change.py')

if __name__ == "__main__":
    main()

