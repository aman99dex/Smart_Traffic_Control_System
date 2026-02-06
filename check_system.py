#!/usr/bin/env python3
"""Quick system check to verify all components work"""

import os
import sys

os.chdir('/Users/aman/Desktop/Density-Based-Smart-Traffic-Control-System-main')

print("Checking system components...")
print("="*60)

try:
    print("\n1. Testing utils module...")
    from utils import config_mgr, logger
    assert config_mgr is not None, "config_mgr is None"
    assert logger is not None, "logger is None"
    print("   ✅ utils module OK")
except Exception as e:
    print(f"   ❌ utils module FAILED: {e}")
    sys.exit(1)

try:
    print("\n2. Testing CannyEdgeDetection...")
    from CannyEdgeDetection import CannyEdgeDetector
    import numpy as np
    # Create a dummy image array for testing
    dummy_image = [np.random.randint(0, 256, (100, 100), dtype=np.uint8)]
    detector = CannyEdgeDetector(dummy_image)
    print("   ✅ CannyEdgeDetection OK")
except Exception as e:
    print(f"   ❌ CannyEdgeDetection FAILED: {e}")
    sys.exit(1)

try:
    print("\n3. Testing Main.py...")
    # Note: Main.py requires Tkinter which is not available in headless mode
    # We'll test that the imports can at least be parsed
    with open('/Users/aman/Desktop/Density-Based-Smart-Traffic-Control-System-main/Main.py', 'r') as f:
        code = f.read()
        # Just verify it can be parsed as valid Python
        compile(code, 'Main.py', 'exec')
    print("   ✅ Main.py (syntax valid - GUI requires display)")
except Exception as e:
    print(f"   ❌ Main.py FAILED: {e}")
    sys.exit(1)

try:
    print("\n4. Testing config values...")
    assert config_mgr.get("application.title") == "Smart Traffic Control System"
    assert config_mgr.get("traffic_density.lanes") == 4
    print("   ✅ Configuration values OK")
except Exception as e:
    print(f"   ❌ Configuration FAILED: {e}")
    sys.exit(1)

try:
    print("\n5. Testing file structure...")
    assert os.path.exists("config.json"), "config.json missing"
    assert os.path.exists("Previous_data.txt"), "Previous_data.txt missing"
    assert os.path.exists("requirements.txt"), "requirements.txt missing"
    print("   ✅ File structure OK")
except Exception as e:
    print(f"   ❌ File structure FAILED: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✅ ALL SYSTEM CHECKS PASSED")
print("✅ SYSTEM IS READY FOR USE")
print("="*60)
