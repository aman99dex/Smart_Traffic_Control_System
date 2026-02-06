# Density Based Smart Traffic Control System

## Overview

A computer vision-based traffic control system that intelligently manages traffic light timing by analyzing real-time traffic density using **Canny Edge Detection** algorithm. The system processes traffic camera images to detect vehicle density across multiple lanes and dynamically allocates green light duration based on actual traffic conditions and historical data patterns.

### Key Features

- **Real-time Traffic Density Detection**: Uses Canny edge detection to identify vehicles in traffic images
- **Multi-Lane Support**: Manages up to 4 traffic lanes simultaneously
- **Dynamic Time Allocation**: Automatically adjusts green light duration (30-60 seconds) based on current traffic density
- **Historical Data Tracking**: Compares current conditions with historical patterns for intelligent optimization
- **GUI Interface**: User-friendly desktop application built with Tkinter for easy operation

## System Architecture

### Image Processing Pipeline

#### 1. Grayscale Conversion
- RGB images are converted to grayscale to simplify processing and improve signal-to-noise ratio
- Formula: `I = 0.2989*R + 0.5870*G + 0.1140*B`

#### 2. Gaussian Filtering
- Applies Gaussian filter to remove noise
- Prevents noise from being misidentified as vehicle edges during detection

#### 3. Canny Edge Detection
- **Gradient Calculation**: Uses Sobel filters to compute image gradients in X and Y directions
- **Non-Maximum Suppression**: Keeps only the most important edges by comparing each pixel with its neighbors
- **Double Thresholding**: Classifies edges as strong, weak, or non-edges using configurable thresholds
- **Hysteresis**: Connects weak edges to strong edges for complete edge continuity

#### 4. Binary Image Conversion
- Converts detected edges to binary images (0 or 1 for each pixel)
- White pixels (1) represent detected vehicle edges

### Traffic Density Analysis

1. **Capture Density**: System records white pixel count when green light is active
2. **Compare Lanes**: Analyzes data from all 4 lanes separately
3. **Historical Comparison**: Compares current density against previous measurements stored in `Previous_data.txt`
4. **Time Allocation**: 
   - Very High Density: 60 seconds
   - High Density: 50 seconds
   - Medium Density: 40 seconds
   - Low Density: 30 seconds

## Requirements

- Python 3.6+
- tkinter (usually comes with Python)
- numpy
- opencv-python (cv2)
- matplotlib
- scipy
- scikit-image

## Installation

### 1. Clone or Download the Repository
```bash
cd /path/to/Density-Based-Smart-Traffic-Control-System-main
```

### 2. Create a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install packages manually:
```bash
pip install numpy opencv-python matplotlib scipy scikit-image
```

### 4. Prepare Directories
Ensure the following directories exist in the project root:
- `images/` - Place traffic camera images here
- `gray/` - Output directory for processed images (auto-created if missing)

## Usage

### Running the Application

```bash
python Main.py
```

This launches a GUI window titled "Green Light Control System" with the following options:

### Step-by-Step Guide

1. **Select Lane Number**: Choose which lane (1-4) you want to analyze from the dropdown menu
2. **Upload Traffic Image**: Click "Upload Traffic Image" to select a traffic camera image from the `images/` folder
3. **Process Image**: Click "Image Preprocessing Using Canny Edge Detection" to detect vehicle edges
4. **Count Pixels**: Click "White Pixel Count" to compare edge pixels between current and reference images
5. **Calculate Time**: Click "Calculate Green Signal Time Allocation" to determine optimal green light duration
6. **Exit**: Click "Exit" to close the application

### Input Requirements

- Place traffic camera images in the `images/` directory
- Images should be in standard formats (PNG, JPG, etc.)
- Ensure you have a reference image named `gray/refrence.png` for comparison

### Output Files

- `gray/test.png` - Processed edge-detected image from current traffic camera
- `Previous_data.txt` - Historical traffic density data for each lane (updated automatically)

## Project Files

| File | Purpose |
|------|---------|
| `Main.py` | Main GUI application and traffic analysis logic |
| `CannyEdgeDetection.py` | Canny edge detection algorithm implementation |
| `test.py` | Testing and utility functions |
| `Previous_data.txt` | Stores historical traffic density for each lane |
| `images/` | Directory for input traffic camera images |
| `gray/` | Directory for processed and output images |

## Technical Details

### Canny Edge Detection Parameters (Configurable)

- **Sigma**: 1.4 (Gaussian filter smoothing)
- **Kernel Size**: 5 (Filter kernel dimensions)
- **Low Threshold**: 0.09 (Lower edge detection threshold)
- **High Threshold**: 0.20 (Upper edge detection threshold)
- **Weak Pixel Value**: 100 (Weak edge intensity)
- **Strong Pixel Value**: 255 (Strong edge intensity)

### Data Storage

The system maintains `Previous_data.txt` with 4 lines (one per lane) containing the white pixel count from the last analysis. This historical data is used to classify traffic density levels.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| No GUI window appears | Ensure tkinter is installed (`python -m tkinter` test) |
| Image file not found | Place images in the `images/` directory |
| `gray/refrence.png` missing | Ensure reference image exists or set it up first |

## How It Works - Example

1. Camera captures traffic image
2. System converts to grayscale and applies Gaussian blur
3. Canny edge detection identifies vehicle outlines
4. Algorithm counts white pixels in detected edges
5. Compares count to historical data:
   - If count > threshold[3]: 60 seconds (very high)
   - If count > threshold[2]: 50 seconds (high)
   - If count > threshold[1]: 40 seconds (medium)
   - If count > threshold[0]: 30 seconds (low)
6. Green light time is allocated and `Previous_data.txt` is updated

## Future Improvements

- Real-time video stream processing
- Multi-intersection coordination
- Machine learning for pattern recognition
- REST API for integration with traffic management systems
- Mobile app for remote monitoring
- Advanced vehicle classification (cars, trucks, motorcycles)

## License

Please refer to the LICENSE file in the repository.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
