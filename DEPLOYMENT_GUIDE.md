# Smart Traffic Control System - Deployment Guide v2.0

## Overview
This guide provides step-by-step instructions for deploying the Smart Traffic Control System to production environments for traffic police and management authorities.

## Pre-Deployment Checklist

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: Minimum 500MB free space
- **Camera Input**: Standard USB webcam or traffic camera feed
- **Network**: Internet connection (for future cloud integration)

### Software Requirements
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment support

## Installation Instructions

### Step 1: Clone Repository
```bash
git clone https://github.com/aman99dex/Smart_Traffic_Control_System.git
cd Smart_Traffic_Control_System
```

### Step 2: Create Virtual Environment
**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python3 test_system.py
```

Expected output: `All tests passed! System is ready for deployment.`

## Configuration

### Customizing for Your Traffic Network

#### 1. Update config.json

Edit `config.json` to match your traffic management needs:

```json
{
  "traffic_density": {
    "lanes": 4,  // Adjust number of lanes
    "time_allocation": {
      "very_high": {
        "green_time_seconds": 60  // Adjust timing as needed
      }
    }
  }
}
```

#### 2. Canny Edge Detection Tuning

Adjust parameters in `config.json` for your camera angles and lighting conditions:

```json
{
  "image_processing": {
    "canny_edge_detection": {
      "sigma": 1.4,        // Increase for blurrier images
      "kernel_size": 5,    // Change if needed
      "low_threshold": 0.09,   // Adjust sensitivity
      "high_threshold": 0.20   // Adjust sensitivity
    }
  }
}
```

## Running the Application

### Start the System
```bash
python3 Main.py
```

### GUI Workflow
1. **Select Lane** - Choose traffic lane (1-4)
2. **Upload Image** - Load traffic camera snapshot
3. **Process Image** - Apply Canny edge detection to identify vehicles
4. **Count Pixels** - Analyze traffic density from detected edges
5. **Calculate Time** - System determines optimal green light duration
6. **View Results** - Check allocation and logs

## Production Setup

### Directory Structure
```
Smart_Traffic_Control_System/
├── Main.py                      # Main application
├── CannyEdgeDetection.py        # Edge detection algorithm
├── utils.py                     # Utilities and managers
├── config.json                  # Configuration file
├── requirements.txt             # Python dependencies
├── test_system.py              # Test suite
├── images/                     # Input traffic images
├── gray/                       # Processed output images
├── logs/                       # Application logs
├── data/                       # Traffic data storage
└── README.md                   # Documentation
```

### Integration with Traffic Management System

#### 1. Input Integration
- **Manual**: Use GUI to select and process images
- **Automated**: Future support for webcam/IP camera feeds
- **Batch Processing**: Process multiple images sequentially

#### 2. Output Integration
The system generates:
- **Previous_data.txt** - Lane-wise traffic density history
- **Logs** - Operation logs with timestamps
- **gray/test.png** - Processed edge-detected image
- **Console Output** - Real-time status updates

### Typical Daily Workflow for Traffic Police

#### Morning Setup
```bash
# 1. Start system
python3 Main.py

# 2. Verify logs
View Logs → Check for any errors

# 3. Reset data (optional)
Reset Data → To start fresh counting
```

#### During Operation
```bash
# For each intersection/lane:
1. Upload traffic image from camera
2. Process image with Canny edge detection
3. Count white pixels (vehicle detection)
4. System automatically calculates and displays:
   - Traffic density level
   - Recommended green light duration (30-60 seconds)
   - Data is automatically saved
```

#### Evening Review
```bash
# Check statistics
View Logs → Review traffic patterns
Check Previous_data.txt → See lane-wise density trends
```

## Monitoring & Maintenance

### Log Files Location
- **Default**: `logs/traffic_control_YYYYMMDD.log`
- **Daily logs**: Created automatically for each day
- **Format**: `TIMESTAMP - LEVEL - MESSAGE`

### View Logs in Application
1. Click "View Logs" button in GUI
2. Latest log file opens automatically

### Common Log Messages

| Message | Meaning |
|---------|---------|
| `Image uploaded: /path/to/image` | Image successfully loaded |
| `Image processed and saved` | Canny detection completed |
| `Traffic data reset` | Manual data reset performed |
| `Lane X updated with pixel count` | Traffic data saved for lane |
| `ERROR: ...` | Operation failed, see details |

### Performance Monitoring

**Check system performance:**
```bash
# View CPU/Memory usage
System Monitor → Running processes

# Check disk space
df -h  # macOS/Linux
disk usage  # Windows
```

### Data Backup

**Automatic backup created when data is updated:**
- Original: `Previous_data.txt`
- Backup: `Previous_data_backup_YYYYMMDD_HHMMSS.txt`

**Manual backup:**
```bash
cp Previous_data.txt Previous_data_backup.txt
```

## Troubleshooting

### Issue: Application won't start
```bash
# Solution: Verify Python installation
python3 --version  # Should be 3.8+

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Issue: "No module named" error
```bash
# Solution: Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Then reinstall
pip install -r requirements.txt
```

### Issue: Image not processing correctly
1. **Check image format** - Ensure PNG, JPG, BMP, or TIFF
2. **Check file size** - Image should be reasonable size
3. **Adjust parameters** - Modify canny thresholds in config.json
4. **Try different lighting** - Poor lighting affects detection

### Issue: Inconsistent time allocations
1. **Update reference image** - Place current traffic image as reference
2. **Recalibrate thresholds** - Adjust config.json parameters
3. **Check lighting conditions** - Ensure consistent camera setup
4. **Review historical data** - Check Previous_data.txt values

## Security Considerations

### For Traffic Police Use

1. **Data Access Control**
   - Keep config.json secured with proper permissions
   - Restrict access to logs and data files

2. **File Integrity**
   - Regular backups of `Previous_data.txt`
   - Version control for configuration changes

3. **Audit Trail**
   - All operations logged automatically
   - View logs regularly for suspicious activities

### Recommended File Permissions (Linux/macOS)
```bash
chmod 600 config.json              # Config file - read/write only
chmod 600 Previous_data.txt        # Data file - protected
chmod 700 logs/                    # Logs directory
```

## Scaling for Multiple Intersections

For multi-intersection management:

1. **Create separate instances** - Run multiple Main.py processes
2. **Network configuration** - Future cloud API integration planned
3. **Centralized dashboard** - Under development for future releases
4. **Data synchronization** - Cloud-based traffic analytics (planned)

## Performance Optimization

### System Optimization
- **Disable antivirus scanning** for processed files
- **Use SSD** for faster image I/O
- **Allocate adequate RAM** - Minimum 4GB
- **Regular maintenance** - Delete old log files weekly

### Algorithm Optimization
- **Kernel size**: Smaller (3) for faster processing, larger (5-7) for better accuracy
- **Thresholds**: Adjust based on camera calibration
- **Sigma**: Higher values for blurred/distant objects

## Support & Maintenance

### Getting Help
1. **Check logs** - Most issues are logged with solutions
2. **Review config.json** - Ensure correct settings
3. **Run tests** - Use `python3 test_system.py` to verify setup
4. **Check README.md** - Detailed documentation

### Regular Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Review logs | Daily | View Logs button |
| Check traffic patterns | Weekly | Analyze Previous_data.txt |
| Archive old logs | Monthly | Delete logs older than 30 days |
| Backup configuration | Monthly | cp config.json config.backup.json |
| System test | Quarterly | python3 test_system.py |

## Upgrade Instructions

### Backing Up Before Upgrade
```bash
# Create backup directory
mkdir backup_`date +%Y%m%d`

# Backup important files
cp -r logs/ backup_`date +%Y%m%d`/
cp Previous_data.txt backup_`date +%Y%m%d`/
cp config.json backup_`date +%Y%m%d`/
```

### Upgrade Process
```bash
# 1. Pull latest code
git pull origin main

# 2. Update dependencies
pip install --upgrade -r requirements.txt

# 3. Run tests
python3 test_system.py

# 4. If all pass, restart application
python3 Main.py
```

## Compliance & Standards

### Road Traffic Standards (India)
- System complies with Indian Road Traffic Regulations
- Supports 4-lane intersections (configurable)
- Green light duration: 30-60 seconds (adjustable)

### Data Format
- Traffic density stored as pixel counts
- International standard image formats (PNG, JPG)
- UTC timestamps in logs

## Conclusion

The Smart Traffic Control System is production-ready for deployment by traffic police and management authorities. Follow this guide for successful deployment and maintenance.

For questions or issues, refer to README.md or create logs for analysis.

---

**Last Updated**: February 6, 2026  
**Version**: 2.0  
**Status**: Production Ready
