# Quick Reference Guide for Traffic Police

## Starting the System

### Windows
1. Double-click `run.bat` file
2. Wait for setup to complete
3. Application will start automatically

### macOS/Linux
1. Open Terminal
2. Navigate to application folder
3. Run: `./run.sh`
4. Application will start

## Daily Workflow

### Step 1: Select Lane
- Choose lane number (1, 2, 3, or 4) from dropdown
- Only one lane can be processed at a time

### Step 2: Upload Image
- Click "Upload Traffic Image"
- Select a traffic photo from images folder
- Image preview appears on left

### Step 3: Process Image
- Click "Process Image (Canny Edge Detection)"
- System analyzes vehicle edges
- Wait for completion (progress bar shows status)

### Step 4: Count Pixels
- Click "White Pixel Count"
- System compares current vs reference traffic
- Results show in popup and results panel

### Step 5: Calculate Time
- Click "Calculate Green Signal Time"
- System determines optimal signal duration
- Results automatically saved

## Understanding the Results

### Traffic Density Levels
| Level | Duration | Density |
|-------|----------|---------|
| Very High | 60 seconds | Extremely congested |
| High | 50 seconds | Heavy traffic |
| Medium | 40 seconds | Moderate traffic |
| Low | 30 seconds | Light traffic |

### Result Example
```
Lane 1 - Very High Traffic Density - 60 second
```
This means: Lane 1 is very congested, keep green light on for 60 seconds

## Important Features

### View Logs
- Click "View Logs" to see all operations
- Shows timestamps and any errors
- Useful for troubleshooting

### Reset Data
- Click "Reset Data" to clear all history
- Only use if starting fresh measurement
- Warning: Cannot be undone!

### Status Bar
- Shows current operation status
- Blue bar at top of window
- Updates in real-time

## Troubleshooting Quick Tips

| Problem | Solution |
|---------|----------|
| No image selected | Click "Upload Traffic Image" and choose a file |
| "Processing" button disabled | Select a lane first from dropdown |
| Image won't process | Check image format (PNG, JPG, BMP supported) |
| Pixel count shows 0 | Ensure image is in gray/test.png after processing |
| Application crashes | Restart and check logs for error details |

## File Locations

| File | Purpose | Location |
|------|---------|----------|
| Traffic Images | Upload here | `images/` folder |
| Processed Images | Output | `gray/` folder |
| Traffic Data | Historical info | `Previous_data.txt` |
| Logs | Error tracking | `logs/` folder |
| Config | Settings | `config.json` |

## Tips for Best Results

1. **Good Lighting**: Ensure traffic images are taken in daylight
2. **Clear View**: Lane should be clearly visible in image
3. **Consistent Camera**: Use same camera position for comparison
4. **Regular Reference**: Update reference image monthly
5. **Document Changes**: Note any system adjustments in logs

## Common Scenarios

### Morning Setup
```
1. Start application
2. Check logs from yesterday (View Logs)
3. Start processing images for the day
4. Reset Data if starting fresh count
```

### During Peak Hours
```
1. Upload traffic image every 5-10 minutes
2. Process immediately
3. Count pixels
4. Calculate time allocation
5. Adjust signal accordingly
```

### Evening Shutdown
```
1. Process final images of the day
2. Review logs for any issues
3. Note any unusual traffic patterns
4. Close application
```

## System Messages Explained

| Message | Meaning | Action |
|---------|---------|--------|
| "Image loaded successfully" | Image file accepted | Proceed to next step |
| "Image processing completed" | Edge detection done | Click "Count Pixels" |
| "Pixel count completed" | Analysis finished | Click "Calculate Time" |
| "Time allocation calculated" | System ready | Data saved automatically |
| "ERROR: ..." | Something failed | Check logs for details |

## Keyboard Shortcuts

| Action | Keyboard |
|--------|----------|
| Exit Application | Alt+F4 (Windows) / Cmd+Q (Mac) |
| Navigate | Tab key |
| Activate Button | Space bar |

## Need Help?

1. **Check Logs**: View Logs button shows all details
2. **Read Guide**: DEPLOYMENT_GUIDE.md has detailed info
3. **Check Config**: config.json has all settings
4. **Run Tests**: `python3 test_system.py` validates system

## Safety Reminders

⚠️ **Important**
- Always upload clear, recent traffic images
- Don't modify config.json without understanding
- Backup Previous_data.txt regularly
- Review logs for system health
- Never reset data during active monitoring

✓ **Do This**
- Keep camera clean for clear images
- Use consistent lighting conditions
- Process images at regular intervals
- Check results for accuracy
- Maintain system as per guide

## Contact & Support

For technical issues:
1. Check DEPLOYMENT_GUIDE.md
2. Review logs (View Logs button)
3. Run test_system.py
4. Check README.md for details

---

**Version**: 2.0  
**Date**: February 6, 2026  
**Status**: Ready for Use
