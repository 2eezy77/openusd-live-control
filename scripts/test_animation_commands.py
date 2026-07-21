"""
Test Animation Commands - Quick verification script

This script tests all the new animation commands to make sure they work
before running the full character_kitchen_walk.py automation.

USAGE:
1. Start Maya with bridge loaded
2. Optionally load any USD scene with animation or create a cube
3. Run: python scripts/test_animation_commands.py

WHAT IT TESTS:
- play command
- stop command  
- set_time command
- get_time command
- (import_fbx tested separately with real file)
"""

import subprocess
import time

def send(cmd):
    """Send command and display result"""
    print(f"\n→ Testing: {cmd}")
    result = subprocess.run(
        f'python scripts/send_cmd.py {cmd}', 
        shell=True, 
        capture_output=True, 
        text=True
    )
    print(f"  Response: {result.stdout.strip()}")
    return result.stdout

def main():
    print("=" * 70)
    print("ANIMATION COMMANDS - QUICK TEST")
    print("=" * 70)
    
    print("\nMake sure Maya is running with bridge loaded!")
    print("Press Enter to start tests...")
    input()
    
    # Test 1: Get current timeline info
    print("\n[TEST 1] Get timeline information")
    send('get_time')
    time.sleep(0.5)
    
    # Test 2: Set to specific frame
    print("\n[TEST 2] Jump to frame 10")
    send('set_time 10')
    time.sleep(0.5)
    
    # Test 3: Jump to another frame
    print("\n[TEST 3] Jump to frame 50")
    send('set_time 50')
    time.sleep(0.5)
    
    # Test 4: Play animation
    print("\n[TEST 4] Play animation")
    send('play')
    time.sleep(2)
    
    # Test 5: Stop animation
    print("\n[TEST 5] Stop animation")
    send('stop')
    time.sleep(0.5)
    
    # Test 6: Play with specific range
    print("\n[TEST 6] Play animation from frame 1 to 100")
    send('play 1 100')
    time.sleep(2)
    
    # Test 7: Stop again
    print("\n[TEST 7] Stop animation")
    send('stop')
    
    print("\n" + "=" * 70)
    print("TESTS COMPLETE!")
    print("=" * 70)
    print("\nExpected results:")
    print("  ✅ All commands should return {\"ok\": true, ...}")
    print("  ✅ Timeline should have moved to different frames")
    print("  ✅ Animation should have started and stopped")
    print("\nIf all tests passed, animation commands are working!")
    print("\nNext: Test import_fbx with a real FBX file:")
    print('  python scripts\\send_cmd.py import_fbx "C:\\path\\to\\file.fbx"')

if __name__ == "__main__":
    main()



