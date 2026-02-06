"""
Test script to validate Smart Traffic Control System
Run tests to ensure all components are working correctly
"""

import sys
import os
import json
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import numpy
        import cv2
        import matplotlib
        import scipy
        import skimage
        from utils import ConfigManager, LoggerSetup, FileManager, TrafficDataManager, DataValidator
        from CannyEdgeDetection import CannyEdgeDetector
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_config():
    """Test if config.json loads correctly"""
    print("\nTesting configuration...")
    try:
        from utils import config_mgr
        
        # Test basic config access
        assert config_mgr.get("application.title") == "Smart Traffic Control System"
        assert config_mgr.get("traffic_density.lanes") == 4
        
        # Test directory config
        images_dir = config_mgr.get_directory("images")
        assert os.path.exists(images_dir)
        
        print("✓ Configuration loaded and validated")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False


def test_data_validation():
    """Test data validation and file management"""
    print("\nTesting data validation...")
    try:
        from utils import config_mgr, DataValidator
        
        validator = DataValidator(config_mgr)
        data_file = config_mgr.get("files.traffic_data", "Previous_data.txt")
        
        # Validate traffic data file
        result = validator.validate_traffic_data_file(data_file)
        assert result == True
        
        # Check file was created/fixed
        assert os.path.exists(data_file)
        
        with open(data_file, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 4  # Should have 4 lanes
        
        print("✓ Data validation successful")
        return True
    except Exception as e:
        print(f"✗ Data validation error: {e}")
        return False


def test_file_manager():
    """Test file manager operations"""
    print("\nTesting file manager...")
    try:
        from utils import FileManager, config_mgr
        
        fm = FileManager()
        
        # Create test image file
        test_file = "test_image.png"
        Path(test_file).touch()
        
        # Test validation
        is_valid, msg = fm.validate_image_file(test_file, config_mgr)
        
        # File is too small but format is correct
        assert "too small" in msg or "valid" in msg.lower()
        
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        
        print("✓ File manager test successful")
        return True
    except Exception as e:
        print(f"✗ File manager error: {e}")
        return False


def test_traffic_data_manager():
    """Test traffic data manager"""
    print("\nTesting traffic data manager...")
    try:
        from utils import config_mgr, TrafficDataManager
        
        tdm = TrafficDataManager(config_mgr)
        
        # Test getting lane data
        data = tdm.get_lane_data()
        assert len(data) == 4
        
        # Test updating lane data
        result = tdm.update_lane_data(1, 100)
        assert result == True
        
        # Verify update
        data = tdm.get_lane_data()
        assert data[0] == 100
        
        # Test traffic level calculation
        level, time = tdm.get_traffic_level(1, 100, 50)
        assert isinstance(level, str)
        assert isinstance(time, int)
        assert time in [30, 40, 50, 60]
        
        print("✓ Traffic data manager test successful")
        return True
    except Exception as e:
        print(f"✗ Traffic data manager error: {e}")
        return False


def test_canny_edge_detector():
    """Test Canny edge detection"""
    print("\nTesting Canny edge detector...")
    try:
        import numpy as np
        from CannyEdgeDetection import CannyEdgeDetector
        
        # Create a simple test image
        test_img = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        
        detector = CannyEdgeDetector([test_img], sigma=1.4, kernel_size=5)
        result = detector.detect()
        
        assert len(result) == 1
        assert result[0].shape == test_img.shape
        
        print("✓ Canny edge detector test successful")
        return True
    except Exception as e:
        print(f"✗ Canny edge detector error: {e}")
        return False


def test_directories():
    """Test directory structure"""
    print("\nTesting directory structure...")
    try:
        from utils import config_mgr
        
        required_dirs = ["images", "output", "logs", "data"]
        
        for dir_key in required_dirs:
            dir_path = config_mgr.get_directory(dir_key)
            assert os.path.exists(dir_path), f"Directory {dir_path} does not exist"
        
        print("✓ Directory structure verified")
        return True
    except Exception as e:
        print(f"✗ Directory error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Smart Traffic Control System - Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_directories,
        test_data_validation,
        test_file_manager,
        test_traffic_data_manager,
        test_canny_edge_detector,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! System is ready for deployment.")
        return 0
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
