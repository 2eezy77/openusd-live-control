"""
Complete System Test - Verify All Functions Work

This script tests EVERY command to ensure the bridge connection works
and all features are functional.

USAGE:
1. Start Maya with bridge loaded
2. Run: python scripts/test_complete_system.py
"""

import subprocess
import time
import json

def send(cmd):
    """Send command and return parsed result"""
    result = subprocess.run(
        f'python scripts/send_cmd.py {cmd}',
        shell=True,
        capture_output=True,
        text=True
    )
    try:
        return json.loads(result.stdout.strip()), result.stdout.strip()
    except:
        return None, result.stdout.strip()

def test_command(name, cmd, expected_ok=True):
    """Test a command and report result"""
    print(f"\n[TEST] {name}")
    print(f"  Command: {cmd}")
    result, output = send(cmd)
    
    if result and result.get("ok") == expected_ok:
        print(f"  ✅ PASS")
        return True
    else:
        print(f"  ❌ FAIL: {output}")
        return False

def main():
    print("=" * 70)
    print("COMPLETE SYSTEM TEST")
    print("=" * 70)
    print("\nTesting all commands to verify bridge connection and functionality...")
    
    tests_passed = 0
    tests_total = 0
    
    # ========================================================================
    # Test 1: Connection
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("SECTION 1: CONNECTION TEST")
    print("=" * 70)
    
    tests_total += 1
    if test_command("List objects", "list_objects"):
        tests_passed += 1
    
    time.sleep(0.5)
    
    # ========================================================================
    # Test 2: Object Creation
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("SECTION 2: OBJECT CREATION")
    print("=" * 70)
    
    tests_total += 1
    if test_command("Create cube", "add_cube /World/TestCube 2"):
        tests_passed += 1
    
    time.sleep(0.5)
    
    # ========================================================================
    # Test 3: Object Manipulation
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("SECTION 3: OBJECT MANIPULATION")
    print("=" * 70)
    
    tests_total += 1
    if test_command("Move object", "set_pose TestCube 0 5 0 0 0 0"):
        tests_passed += 1
    time.sleep(0.3)
    
    tests_total += 1
    if test_command("Rotate object", "set_pose TestCube 0 5 0 0 45 0"):
        tests_passed += 1
    time.sleep(0.3)
    
    # ========================================================================
    # Test 4: Color Control
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("SECTION 4: COLOR CONTROL")
    print("=" * 70)
    
    colors = ['red', 'blue', 'green', 'yellow', 'cyan']
    for color in colors:
        tests_total += 1
        if test_command(f"Set color {color}", f"set_color TestCube {color}"):
            tests_passed += 1
        time.sleep(0.3)
    
    # ========================================================================
    # Test 5: Visibility
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("SECTION 5: VISIBILITY CONTROL")
    print("=" * 70)
    
    tests_total += 1
    if test_command("Hide object", "vis TestCube false"):
        tests_passed += 1
    time.sleep(0.5)
    
    tests_total += 1
    if test_command("Show object", "vis TestCube true"):
        tests_passed += 1
    time.sleep(0.5)
    
    # ========================================================================
    # Test 6: Camera Control
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("SECTION 6: CAMERA CONTROL")
    print("=" * 70)
    
    tests_total += 1
    if test_command("Position camera", "set_camera persp 10 10 10 -30 30 0"):
        tests_passed += 1
    time.sleep(0.5)
    
    # ========================================================================
    # Test 7: Animation Commands
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("SECTION 7: ANIMATION CONTROL")
    print("=" * 70)
    
    tests_total += 1
    if test_command("Get timeline info", "get_time"):
        tests_passed += 1
    time.sleep(0.3)
    
    tests_total += 1
    if test_command("Set frame", "set_time 10"):
        tests_passed += 1
    time.sleep(0.3)
    
    tests_total += 1
    if test_command("Play animation", "play"):
        tests_passed += 1
    time.sleep(0.5)
    
    tests_total += 1
    if test_command("Stop animation", "stop"):
        tests_passed += 1
    time.sleep(0.3)
    
    # ========================================================================
    # Test 8: Object Deletion
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("SECTION 8: OBJECT DELETION")
    print("=" * 70)
    
    tests_total += 1
    if test_command("Delete object", "rm TestCube"):
        tests_passed += 1
    time.sleep(0.5)
    
    # ========================================================================
    # Test 9: Multiple Objects
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("SECTION 9: MULTIPLE OBJECTS")
    print("=" * 70)
    
    # Create multiple objects
    for i in range(3):
        tests_total += 1
        if test_command(f"Create Box{i}", f"add_cube /World/Box{i} 1"):
            tests_passed += 1
        time.sleep(0.2)
    
    # Position them
    positions = [(0, 2, 0), (3, 2, 0), (6, 2, 0)]
    for i, (x, y, z) in enumerate(positions):
        tests_total += 1
        if test_command(f"Position Box{i}", f"set_pose Box{i} {x} {y} {z} 0 0 0"):
            tests_passed += 1
        time.sleep(0.2)
    
    # Color them differently
    colors = ['red', 'yellow', 'blue']
    for i, color in enumerate(colors):
        tests_total += 1
        if test_command(f"Color Box{i} {color}", f"set_color Box{i} {color}"):
            tests_passed += 1
        time.sleep(0.2)
    
    # Clean up
    for i in range(3):
        tests_total += 1
        if test_command(f"Delete Box{i}", f"rm Box{i}"):
            tests_passed += 1
        time.sleep(0.2)
    
    # ========================================================================
    # Final Results
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    
    print(f"\nTests Passed: {tests_passed}/{tests_total}")
    print(f"Success Rate: {(tests_passed/tests_total)*100:.1f}%")
    
    if tests_passed == tests_total:
        print("\n🎉 ALL TESTS PASSED! System is working perfectly!")
        print("\n✅ Your installation is complete and functional.")
        print("✅ All commands are working correctly.")
        print("✅ Bridge connection is stable.")
        print("\nYou're ready to use the system! 🚀")
        return True
    else:
        print(f"\n⚠️  {tests_total - tests_passed} test(s) failed.")
        print("\nTroubleshooting:")
        print("1. Check Maya Script Editor for errors")
        print("2. Verify bridge is loaded and listening")
        print("3. Check object names in Maya Outliner")
        print("4. Try reloading bridge in Maya")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print("\n1. Try demo scripts:")
        print("   python scripts\\box_color_change.py")
        print("   python scripts\\warehouse_box_scanner.py")
        print("\n2. Read guides:")
        print("   MASTER_GUIDE.md - Complete system guide")
        print("   WAREHOUSE_PROJECT_GUIDE.md - Warehouse project")
        print("\n3. Build your own automation!")

