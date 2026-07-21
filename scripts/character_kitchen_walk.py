"""
Character Kitchen Walk - Automated character movement through Pixar kitchen scene

This script loads an ActorCore character with walk animation and a Pixar kitchen scene,
then makes the character walk through predefined waypoints around the kitchen.

USAGE:
1. Start Maya with bridge loaded (run_maya.bat, then load maya_bridge.py)
2. Update the file paths below to match your Downloads folder
3. Run: python scripts/character_kitchen_walk.py

WHAT IT DOES:
- Loads FBX character (has built-in walk animation)
- Loads Pixar kitchen USD scene
- Plays character's walk animation
- Moves character through waypoints (simulates walking around kitchen)

NOTE: You'll need to adjust waypoints after loading to avoid collisions!
"""

import subprocess
import time
import sys

def send(cmd):
    """Send command to Maya bridge and return result"""
    result = subprocess.run(
        f'python scripts/send_cmd.py {cmd}', 
        shell=True, 
        capture_output=True, 
        text=True
    )
    print(result.stdout)
    return result.stdout

def main():
    print("=" * 80)
    print("CHARACTER KITCHEN WALK - Automated Scene Setup")
    print("=" * 80)
    
    # ========================================================================
    # CONFIGURATION - UPDATE THESE PATHS!
    # ========================================================================
    
    # Character FBX path (UPDATE THIS to match your Downloads folder!)
    character_fbx = r"C:\Users\Isaac\Downloads\Actorcore-Maya-1102-284522\Actor\party-m-0001\party-m-0001.fbx"
    
    # Kitchen USD path (UPDATE THIS to match your Downloads folder!)
    kitchen_usd = r"C:\Users\Isaac\Downloads\Kitchen_set\Kitchen_set\Kitchen_set.usd"
    
    # Character root node name (check Maya Outliner after loading)
    # This might be "party_m_0001", "Hips", "Root", etc.
    # You'll need to verify this in Maya and update it!
    character_root = "party_m_0001"
    
    # ========================================================================
    # LOAD ASSETS
    # ========================================================================
    
    print("\n[1/4] Loading character FBX...")
    print(f"      Path: {character_fbx}")
    send(f'import_fbx "{character_fbx}"')
    
    print("\n[2/4] Loading kitchen USD...")
    print(f"      Path: {kitchen_usd}")
    send(f'open "{kitchen_usd}"')
    
    # Give Maya a moment to load everything
    time.sleep(2)
    
    # ========================================================================
    # START ANIMATION
    # ========================================================================
    
    print("\n[3/4] Starting walk animation...")
    send('play')
    
    # ========================================================================
    # WALK THROUGH WAYPOINTS
    # ========================================================================
    
    print("\n[4/4] Walking character through kitchen...")
    
    # PLACEHOLDER WAYPOINTS - You'll need to refine these!
    # Format: (x, y, z, rotation_y)
    # These are just guesses - adjust after seeing kitchen layout
    waypoints = [
        (0, 0, 0, 0),           # Start at origin
        (3, 0, 0, 0),           # Walk forward
        (3, 0, 3, 90),          # Turn right
        (6, 0, 3, 90),          # Along counter (maybe?)
        (6, 0, 6, 180),         # Around table (maybe?)
        (3, 0, 6, 180),         # Walk back
        (0, 0, 6, 270),         # Turn toward entrance
        (0, 0, 0, 0),           # Back to start
    ]
    
    print(f"\n   Character will visit {len(waypoints)} waypoints:")
    for i, (x, y, z, ry) in enumerate(waypoints):
        print(f"   #{i+1}: Position ({x}, {y}, {z}), Rotation Y={ry}°")
    
    print("\n   Starting walk in 2 seconds...")
    time.sleep(2)
    
    for i, (x, y, z, ry) in enumerate(waypoints):
        print(f"\n   → Waypoint {i+1}/{len(waypoints)}: ({x}, {y}, {z}) @ {ry}°")
        send(f'set_pose {character_root} {x} {y} {z} 0 {ry} 0')
        time.sleep(2)  # Let walk animation play for 2 seconds
    
    print("\n[COMPLETE] Walk finished!")
    print("\nNext steps:")
    print("1. Check Maya Outliner to verify character root node name")
    print("2. Manually position character to find safe waypoints")
    print("3. Update waypoints list in this script")
    print("4. Run again with refined waypoints!")
    
    # Optionally stop animation
    # send('stop')

if __name__ == "__main__":
    main()

