"""
Utility module for the Smart Traffic Control System.
Provides logging, configuration management, data validation, and file operations.
"""

import json
import os
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class ConfigManager:
    """Manages application configuration from config.json"""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize ConfigManager and load configuration"""
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            # Only log if logger is available (check if logger has been defined globally)
            try:
                if 'logger' in globals():
                    logger.info(f"Configuration loaded successfully from {self.config_path}")
            except:
                pass
            
            return config
        except json.JSONDecodeError as e:
            try:
                if 'logger' in globals():
                    logger.error(f"Invalid JSON in configuration file: {e}")
            except:
                pass
            raise
        except Exception as e:
            try:
                if 'logger' in globals():
                    logger.error(f"Error loading configuration: {e}")
            except:
                pass
            raise
    
    def get(self, key: str, default=None):
        """Get configuration value using dot notation (e.g., 'image_processing.canny_edge_detection.sigma')"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def get_directory(self, dir_key: str) -> str:
        """Get directory path and create if not exists"""
        dir_path = self.get(f"directories.{dir_key}")
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            # Only log if logger is already initialized
            try:
                if 'logger' in globals():
                    logger.info(f"Created directory: {dir_path}")
            except:
                pass
        return dir_path


class LoggerSetup:
    """Setup application logging"""
    
    @staticmethod
    def setup_logger(name: str = "TrafficControlSystem", config: ConfigManager = None) -> logging.Logger:
        """Setup and return a logger instance"""
        logger_instance = logging.getLogger(name)
        
        # Only add handlers if not already configured
        if not logger_instance.handlers:
            # Get logging config
            if config:
                log_level = config.get("logging.level", "INFO")
                log_format = config.get("logging.format", "%(asctime)s - %(levelname)s - %(message)s")
                date_format = config.get("logging.date_format", "%Y-%m-%d %H:%M:%S")
                log_dir = config.get_directory("logs")
            else:
                log_level = "INFO"
                log_format = "%(asctime)s - %(levelname)s - %(message)s"
                date_format = "%Y-%m-%d %H:%M:%S"
                log_dir = "logs"
            
            # Set logger level
            logger_instance.setLevel(getattr(logging, log_level))
            
            # Create formatter
            formatter = logging.Formatter(log_format, datefmt=date_format)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger_instance.addHandler(console_handler)
            
            # File handler
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"traffic_control_{datetime.now().strftime('%Y%m%d')}.log")
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger_instance.addHandler(file_handler)
        
        return logger_instance


# Initialize global logger
try:
    config_mgr = ConfigManager()
    logger = LoggerSetup.setup_logger("TrafficControlSystem", config_mgr)
except Exception as e:
    # Fallback if config doesn't exist
    import logging
    import traceback
    config_mgr = None
    logger = logging.getLogger("TrafficControlSystem")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    # Print error for debugging
    logger.error(f"Failed to initialize from config: {e}")
    traceback.print_exc()


class DataValidator:
    """Validate traffic data and file integrity"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.num_lanes = config.get("traffic_density.lanes", 4)
    
    def validate_traffic_data_file(self, filepath: str) -> bool:
        """Validate Previous_data.txt file structure and content"""
        try:
            if not os.path.exists(filepath):
                logger.warning(f"Traffic data file not found: {filepath}. Creating new file.")
                self._create_traffic_data_file(filepath)
                return True
            
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            # Check if file has correct number of lanes
            if len(lines) != self.num_lanes:
                logger.warning(f"Traffic data file has {len(lines)} lines, expected {self.num_lanes}. Recreating file.")
                self._create_traffic_data_file(filepath)
                return True
            
            # Validate each line contains a valid number
            for i, line in enumerate(lines):
                try:
                    int(line.strip())
                except ValueError:
                    logger.warning(f"Invalid data in lane {i+1}: {line.strip()}. Resetting to 0.")
                    lines[i] = "0\n"
            
            # Write corrected data if any issues found
            with open(filepath, 'w') as f:
                f.writelines(lines)
            
            logger.info(f"Traffic data file validated: {filepath}")
            return True
        
        except Exception as e:
            logger.error(f"Error validating traffic data file: {e}")
            return False
    
    def _create_traffic_data_file(self, filepath: str):
        """Create a new traffic data file with default values"""
        try:
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
            with open(filepath, 'w') as f:
                for _ in range(self.num_lanes):
                    f.write("0\n")
            logger.info(f"Created new traffic data file: {filepath}")
        except Exception as e:
            logger.error(f"Error creating traffic data file: {e}")
            raise
    
    def backup_traffic_data(self, source: str, dest: str = None):
        """Create backup of traffic data file"""
        try:
            if not os.path.exists(source):
                return False
            
            if dest is None:
                dest = source.replace(".txt", f"_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            
            shutil.copy2(source, dest)
            logger.info(f"Backup created: {dest}")
            return True
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False


class FileManager:
    """Manage file operations with error handling"""
    
    @staticmethod
    def validate_image_file(filepath: str, config: ConfigManager) -> Tuple[bool, str]:
        """Validate if image file is valid and supported"""
        try:
            if not os.path.exists(filepath):
                return False, f"File not found: {filepath}"
            
            # Check file extension
            valid_formats = config.get("validation.supported_formats", ["png", "jpg", "jpeg", "bmp", "tiff"])
            file_ext = os.path.splitext(filepath)[1].lower().lstrip('.')
            
            if file_ext not in valid_formats:
                return False, f"Unsupported image format: {file_ext}. Supported: {', '.join(valid_formats)}"
            
            # Check file size
            file_size = os.path.getsize(filepath)
            min_size = config.get("validation.min_image_size", 100)
            max_size = config.get("validation.max_image_size", 10000) * 1024  # Convert to bytes
            
            if file_size < min_size:
                return False, f"Image file too small: {file_size} bytes"
            
            if file_size > max_size:
                return False, f"Image file too large: {file_size} bytes (max: {max_size} bytes)"
            
            logger.info(f"Image file validated: {filepath}")
            return True, "Image file is valid"
        
        except Exception as e:
            error_msg = f"Error validating image file: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    @staticmethod
    def ensure_directory_exists(directory: str) -> bool:
        """Create directory if it doesn't exist"""
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {e}")
            return False


class TrafficDataManager:
    """Manage traffic density data operations"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.data_file = config.get("files.traffic_data", "Previous_data.txt")
        self.backup_file = config.get("files.traffic_data_backup", "Previous_data_backup.txt")
        self.num_lanes = config.get("traffic_density.lanes", 4)
        self.validator = DataValidator(config)
        
        # Initialize/validate data file
        self.validator.validate_traffic_data_file(self.data_file)
    
    def get_lane_data(self) -> List[int]:
        """Get traffic data for all lanes"""
        try:
            with open(self.data_file, 'r') as f:
                lines = f.readlines()
            
            data = []
            for line in lines:
                try:
                    data.append(int(line.strip()))
                except ValueError:
                    data.append(0)
            
            return data
        except Exception as e:
            logger.error(f"Error reading lane data: {e}")
            return [0] * self.num_lanes
    
    def update_lane_data(self, lane: int, pixel_count: int) -> bool:
        """Update traffic data for a specific lane"""
        try:
            if lane < 1 or lane > self.num_lanes:
                logger.error(f"Invalid lane number: {lane}")
                return False
            
            # Backup before updating
            self.validator.backup_traffic_data(self.data_file, self.backup_file)
            
            data = self.get_lane_data()
            data[lane - 1] = pixel_count
            
            with open(self.data_file, 'w') as f:
                for value in data:
                    f.write(f"{value}\n")
            
            logger.info(f"Lane {lane} updated with pixel count: {pixel_count}")
            return True
        
        except Exception as e:
            logger.error(f"Error updating lane data: {e}")
            return False
    
    def get_traffic_level(self, lane: int, sample_pixels: int, reference_pixels: int) -> Tuple[str, int]:
        """
        Determine traffic density level and green light time
        
        Args:
            lane: Lane number (1-4)
            sample_pixels: Current white pixel count
            reference_pixels: Reference white pixel count
        
        Returns:
            Tuple of (traffic_level_label, green_time_seconds)
        """
        try:
            data = self.get_lane_data()
            threshold_4 = data[0] if len(data) > 0 else 0
            threshold_3 = data[1] if len(data) > 1 else 0
            threshold_2 = data[2] if len(data) > 2 else 0
            threshold_1 = data[3] if len(data) > 3 else 0
            
            count = 0
            if sample_pixels >= threshold_4:
                count += 1
            if sample_pixels >= threshold_3:
                count += 1
            if sample_pixels >= threshold_2:
                count += 1
            if sample_pixels >= threshold_1:
                count += 1
            
            time_config = self.config.get("traffic_density.time_allocation")
            
            if count == 4:
                level = time_config["very_high"]["label"]
                time = time_config["very_high"]["green_time_seconds"]
            elif count == 3:
                level = time_config["high"]["label"]
                time = time_config["high"]["green_time_seconds"]
            elif count == 2:
                level = time_config["medium"]["label"]
                time = time_config["medium"]["green_time_seconds"]
            else:
                level = time_config["low"]["label"]
                time = time_config["low"]["green_time_seconds"]
            
            logger.info(f"Traffic level determined: {level} ({time}s) for lane {lane}")
            return level, time
        
        except Exception as e:
            logger.error(f"Error determining traffic level: {e}")
            return "Error", 30


# Export main utilities
__all__ = ['ConfigManager', 'LoggerSetup', 'DataValidator', 'FileManager', 
           'TrafficDataManager', 'logger', 'config_mgr']
