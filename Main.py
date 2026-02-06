"""
Main GUI application for Smart Traffic Control System
Implements a production-ready traffic control interface with threading and error handling
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import matplotlib.image as mpimg
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime

from CannyEdgeDetection import CannyEdgeDetector
from utils import (ConfigManager, LoggerSetup, FileManager, TrafficDataManager, 
                   logger, config_mgr)


class TrafficControlGUI:
    """Main GUI application class for Smart Traffic Control System"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.config = config_mgr
        self.setup_logger()
        self.setup_directories()
        
        # Initialize managers
        self.file_manager = FileManager()
        self.traffic_manager = TrafficDataManager(self.config)
        
        # GUI variables
        self.selected_lane = tk.StringVar(self.root, value="Select Lane")
        self.filename = None
        self.reference_pixels = 0
        self.sample_pixels = 0
        self.processing = False
        
        logger.info("Initializing GUI application")
        self.setup_gui()
    
    def setup_logger(self):
        """Setup logging"""
        self.logger = logger
    
    def setup_directories(self):
        """Create required directories"""
        try:
            for dir_key in ["images", "output", "logs", "data"]:
                self.config.get_directory(dir_key)
            self.logger.info("All required directories created/verified")
        except Exception as e:
            self.logger.error(f"Error setting up directories: {e}")
            messagebox.showerror("Directory Error", f"Failed to create directories: {e}")
    
    def setup_gui(self):
        """Setup the GUI components"""
        try:
            # Window configuration
            window_title = self.config.get("gui.window_title", "Green Light Control System")
            window_width = self.config.get("gui.window_width", 1300)
            window_height = self.config.get("gui.window_height", 1200)
            
            self.root.title(window_title)
            self.root.geometry(f"{window_width}x{window_height}")
            self.root.config(bg='white')
            
            # Font configuration
            font_family = self.config.get("gui.font.family", "Times New Roman")
            font_size = self.config.get("gui.font.size", 14)
            font_style = self.config.get("gui.font.style", "bold")
            self.font_main = (font_family, font_size, font_style)
            self.font_small = (font_family, 10, "normal")
            
            # Create main frame
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Title Label
            title_label = tk.Label(main_frame, text=window_title, font=(font_family, 20, "bold"))
            title_label.pack(pady=10)
            
            # Status Bar
            self.status_var = tk.StringVar(value="Ready")
            self.status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                                       bg='lightblue', fg='black', font=self.font_small)
            self.status_bar.pack(fill=tk.X, pady=5)
            
            # Lane Selection Frame
            lane_frame = ttk.LabelFrame(main_frame, text="Lane Selection", padding="10")
            lane_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(lane_frame, text="Select Lane:", font=self.font_main).pack(side=tk.LEFT, padx=5)
            
            lane_menu = ttk.OptionMenu(lane_frame, self.selected_lane, "Select Lane", 
                                       "Lane 1", "Lane 2", "Lane 3", "Lane 4",
                                       command=self.on_lane_selected)
            lane_menu.pack(side=tk.LEFT, padx=5)
            
            # Image Input Frame
            input_frame = ttk.LabelFrame(main_frame, text="Image Input", padding="10")
            input_frame.pack(fill=tk.X, padx=10, pady=5)
            
            upload_btn = tk.Button(input_frame, text="Upload Traffic Image", 
                                   command=self.upload_traffic_image, font=self.font_main)
            upload_btn.pack(side=tk.LEFT, padx=5)
            
            self.path_label = tk.Label(input_frame, text="No image selected", 
                                       bg='orange', fg='white', font=self.font_small, 
                                       wraplength=500, justify=tk.LEFT)
            self.path_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            
            # Preview Frame
            preview_frame = ttk.LabelFrame(main_frame, text="Image Preview", padding="10")
            preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            self.preview_label = tk.Label(preview_frame, text="Image preview will appear here", 
                                         bg='lightgray', font=self.font_small)
            self.preview_label.pack(fill=tk.BOTH, expand=True)
            
            # Processing Frame
            process_frame = ttk.LabelFrame(main_frame, text="Image Processing", padding="10")
            process_frame.pack(fill=tk.X, padx=10, pady=5)
            
            process_btn = tk.Button(process_frame, text="Process Image (Canny Edge Detection)", 
                                   command=self.apply_canny, font=self.font_main, 
                                   bg='lightblue', state=tk.DISABLED)
            process_btn.pack(side=tk.LEFT, padx=5)
            self.process_btn = process_btn
            
            # Progress bar
            self.progress = ttk.Progressbar(process_frame, mode='indeterminate')
            self.progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            
            # Analysis Frame
            analysis_frame = ttk.LabelFrame(main_frame, text="Traffic Analysis", padding="10")
            analysis_frame.pack(fill=tk.X, padx=10, pady=5)
            
            count_btn = tk.Button(analysis_frame, text="Count Pixels", 
                                 command=self.pixel_count, font=self.font_main, 
                                 bg='lightyellow', state=tk.DISABLED)
            count_btn.pack(side=tk.LEFT, padx=5)
            self.count_btn = count_btn
            
            time_btn = tk.Button(analysis_frame, text="Calculate Green Signal Time", 
                                command=self.time_allocation, font=self.font_main, 
                                bg='lightgreen', state=tk.DISABLED)
            time_btn.pack(side=tk.LEFT, padx=5)
            self.time_btn = time_btn
            
            # Results Frame
            results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
            results_frame.pack(fill=tk.X, padx=10, pady=5)
            
            self.results_text = tk.Text(results_frame, height=6, width=80, 
                                       font=self.font_small, state=tk.DISABLED)
            self.results_text.pack(fill=tk.BOTH, expand=True)
            
            # Action Frame
            action_frame = ttk.Frame(main_frame, padding="10")
            action_frame.pack(fill=tk.X, padx=10, pady=5)
            
            view_logs_btn = tk.Button(action_frame, text="View Logs", 
                                     command=self.view_logs, font=self.font_main)
            view_logs_btn.pack(side=tk.LEFT, padx=5)
            
            reset_btn = tk.Button(action_frame, text="Reset Data", 
                                 command=self.reset_data, font=self.font_main)
            reset_btn.pack(side=tk.LEFT, padx=5)
            
            exit_btn = tk.Button(action_frame, text="Exit", 
                                command=self.exit_app, font=self.font_main, bg='lightcoral')
            exit_btn.pack(side=tk.RIGHT, padx=5)
            
            self.logger.info("GUI setup completed successfully")
        
        except Exception as e:
            self.logger.error(f"Error setting up GUI: {e}")
            messagebox.showerror("GUI Setup Error", f"Failed to setup GUI: {e}")
    
    def on_lane_selected(self, value):
        """Handle lane selection"""
        if value != "Select Lane":
            self.logger.info(f"Lane selected: {value}")
            self.status_var.set(f"Selected: {value}")
            self.process_btn.config(state=tk.NORMAL)
        else:
            self.process_btn.config(state=tk.DISABLED)
    
    def update_status(self, message: str):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def append_results(self, message: str):
        """Append message to results text widget"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def upload_traffic_image(self):
        """Upload traffic image with validation"""
        try:
            self.update_status("Selecting image...")
            
            images_dir = self.config.get("directories.images", "images")
            self.filename = filedialog.askopenfilename(
                initialdir=images_dir,
                title="Select Traffic Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                          ("PNG files", "*.png"),
                          ("JPG files", "*.jpg *.jpeg"),
                          ("All files", "*.*")]
            )
            
            if not self.filename:
                self.update_status("Image selection cancelled")
                return
            
            # Validate image
            is_valid, error_msg = self.file_manager.validate_image_file(self.filename, self.config)
            if not is_valid:
                messagebox.showerror("Invalid Image", error_msg)
                self.logger.error(f"Invalid image: {error_msg}")
                self.update_status("Invalid image selected")
                return
            
            self.path_label.config(text=f"Selected: {self.filename}")
            self.logger.info(f"Image uploaded: {self.filename}")
            self.update_status("Image loaded successfully")
            self.count_btn.config(state=tk.NORMAL)
            
            # Show preview
            self.show_preview()
        
        except Exception as e:
            self.logger.error(f"Error uploading image: {e}")
            messagebox.showerror("Upload Error", f"Failed to upload image: {e}")
            self.update_status("Error uploading image")
    
    def show_preview(self):
        """Show image preview"""
        try:
            if not self.filename:
                return
            
            # Load and resize image for preview
            img = cv2.imread(self.filename)
            if img is None:
                return
            
            # Resize for preview (max 200x200)
            h, w = img.shape[:2]
            max_size = 200
            if h > max_size or w > max_size:
                scale = max_size / max(h, w)
                img = cv2.resize(img, (int(w * scale), int(h * scale)))
            
            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Convert to PhotoImage format
            from PIL import Image, ImageTk
            pil_img = Image.fromarray(img)
            photo = ImageTk.PhotoImage(pil_img)
            
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo  # Keep a reference
        
        except ImportError:
            self.preview_label.config(text="Install Pillow for image preview: pip install Pillow")
        except Exception as e:
            self.logger.error(f"Error showing preview: {e}")
    
    def rgb2gray(self, rgb):
        """Convert RGB to grayscale"""
        r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        r_weight = self.config.get("image_processing.grayscale_conversion.r_weight", 0.2989)
        g_weight = self.config.get("image_processing.grayscale_conversion.g_weight", 0.5870)
        b_weight = self.config.get("image_processing.grayscale_conversion.b_weight", 0.1140)
        
        gray = r_weight * r + g_weight * g + b_weight * b
        return gray
    
    def apply_canny_thread(self):
        """Apply Canny edge detection in a separate thread"""
        try:
            if not self.filename:
                messagebox.showerror("Error", "Please upload an image first")
                return
            
            self.update_status("Processing image with Canny edge detection...")
            self.progress.start()
            
            # Load image
            img = mpimg.imread(self.filename)
            img_gray = self.rgb2gray(img)
            
            # Apply Canny edge detection
            sigma = self.config.get("image_processing.canny_edge_detection.sigma", 1.4)
            kernel_size = self.config.get("image_processing.canny_edge_detection.kernel_size", 5)
            low_threshold = self.config.get("image_processing.canny_edge_detection.low_threshold", 0.09)
            high_threshold = self.config.get("image_processing.canny_edge_detection.high_threshold", 0.20)
            weak_pixel = self.config.get("image_processing.canny_edge_detection.weak_pixel", 100)
            strong_pixel = self.config.get("image_processing.canny_edge_detection.strong_pixel", 255)
            
            detector = CannyEdgeDetector(
                [img_gray],
                sigma=sigma,
                kernel_size=kernel_size,
                lowthreshold=low_threshold,
                highthreshold=high_threshold,
                weak_pixel=weak_pixel,
                strong_pixel=strong_pixel
            )
            
            detected_imgs = detector.detect()
            
            # Save processed image
            output_dir = self.config.get("directories.output", "gray")
            output_file = f"{output_dir}/test.png"
            cv2.imwrite(output_file, detected_imgs[0])
            
            self.logger.info(f"Image processed and saved: {output_file}")
            self.append_results(f"Image processed successfully - Saved to {output_file}")
            self.update_status("Image processing completed")
            self.count_btn.config(state=tk.NORMAL)
        
        except Exception as e:
            self.logger.error(f"Error in Canny edge detection: {e}")
            self.append_results(f"ERROR: {e}")
            messagebox.showerror("Processing Error", f"Failed to process image: {e}")
            self.update_status("Error processing image")
        
        finally:
            self.progress.stop()
            self.processing = False
            self.process_btn.config(state=tk.NORMAL)
    
    def apply_canny(self):
        """Apply Canny edge detection"""
        if self.processing:
            messagebox.showwarning("Processing", "Image processing is already in progress")
            return
        
        self.processing = True
        self.process_btn.config(state=tk.DISABLED)
        
        # Run in separate thread to prevent GUI freeze
        thread = threading.Thread(target=self.apply_canny_thread, daemon=True)
        thread.start()
    
    def pixel_count(self):
        """Count white pixels in processed image"""
        try:
            self.update_status("Counting pixels...")
            
            output_dir = self.config.get("directories.output", "gray")
            test_file = f"{output_dir}/test.png"
            ref_file = self.config.get("files.reference_image", f"{output_dir}/refrence.png")
            
            if not Path(test_file).exists():
                messagebox.showerror("Error", "Processed image not found. Process an image first.")
                return
            
            if not Path(ref_file).exists():
                messagebox.showwarning("Warning", f"Reference image not found: {ref_file}\nUsing test image as reference.")
                ref_file = test_file
            
            # Read images in grayscale
            img_test = cv2.imread(test_file, cv2.IMREAD_GRAYSCALE)
            img_ref = cv2.imread(ref_file, cv2.IMREAD_GRAYSCALE)
            
            if img_test is None:
                messagebox.showerror("Error", "Failed to read processed image")
                return
            
            if img_ref is None:
                messagebox.showerror("Error", "Failed to read reference image")
                return
            
            # Count white pixels
            self.sample_pixels = np.sum(img_test == 255)
            self.reference_pixels = np.sum(img_ref == 255)
            
            self.logger.info(f"Pixel count - Sample: {self.sample_pixels}, Reference: {self.reference_pixels}")
            
            message = f"Sample White Pixels: {self.sample_pixels}\nReference White Pixels: {self.reference_pixels}"
            messagebox.showinfo("Pixel Count", message)
            self.append_results(f"Pixel Count - Sample: {self.sample_pixels}, Reference: {self.reference_pixels}")
            self.update_status("Pixel count completed")
            self.time_btn.config(state=tk.NORMAL)
        
        except Exception as e:
            self.logger.error(f"Error counting pixels: {e}")
            messagebox.showerror("Pixel Count Error", f"Failed to count pixels: {e}")
            self.update_status("Error counting pixels")
    
    def time_allocation(self):
        """Calculate green signal time allocation"""
        try:
            if self.selected_lane.get() == "Select Lane":
                messagebox.showerror("Error", "Please select a lane first")
                return
            
            if self.sample_pixels == 0:
                messagebox.showerror("Error", "Please count pixels first")
                return
            
            self.update_status("Calculating green light duration...")
            
            lane_num = int(self.selected_lane.get().split()[-1])
            
            # Get traffic level and time
            traffic_level, green_time = self.traffic_manager.get_traffic_level(
                lane_num, self.sample_pixels, self.reference_pixels
            )
            
            # Update data file
            self.traffic_manager.update_lane_data(lane_num, self.sample_pixels)
            
            message = f"Lane {lane_num}\n{traffic_level}\nGreen Light Duration: {green_time} seconds"
            messagebox.showinfo("Time Allocation", message)
            
            self.append_results(f"Lane {lane_num} - {traffic_level} - {green_time}s")
            self.logger.info(f"Time allocation: Lane {lane_num} - {traffic_level} - {green_time}s")
            self.update_status("Time allocation calculated")
        
        except Exception as e:
            self.logger.error(f"Error in time allocation: {e}")
            messagebox.showerror("Calculation Error", f"Failed to calculate time: {e}")
            self.update_status("Error calculating time allocation")
    
    def view_logs(self):
        """View application logs"""
        try:
            log_dir = self.config.get("directories.logs", "logs")
            log_files = list(Path(log_dir).glob("*.log"))
            
            if not log_files:
                messagebox.showinfo("Logs", "No log files found")
                return
            
            # Get the latest log file
            latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
            
            with open(latest_log, 'r') as f:
                log_content = f.read()
            
            # Display in new window
            log_window = tk.Toplevel(self.root)
            log_window.title("Application Logs")
            log_window.geometry("800x600")
            
            text_widget = tk.Text(log_window, font=self.font_small)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert(tk.END, log_content)
            text_widget.config(state=tk.DISABLED)
            
            scrollbar = ttk.Scrollbar(text_widget)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_widget.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=text_widget.yview)
        
        except Exception as e:
            self.logger.error(f"Error viewing logs: {e}")
            messagebox.showerror("Error", f"Failed to view logs: {e}")
    
    def reset_data(self):
        """Reset all traffic data"""
        try:
            if messagebox.askyesno("Confirm", "Reset all lane data? This cannot be undone."):
                data_file = self.config.get("files.traffic_data", "Previous_data.txt")
                num_lanes = self.config.get("traffic_density.lanes", 4)
                
                with open(data_file, 'w') as f:
                    for _ in range(num_lanes):
                        f.write("0\n")
                
                self.logger.info("Traffic data reset")
                messagebox.showinfo("Success", "All lane data has been reset")
                self.append_results("All lane data reset")
                self.update_status("Data reset completed")
        
        except Exception as e:
            self.logger.error(f"Error resetting data: {e}")
            messagebox.showerror("Error", f"Failed to reset data: {e}")
    
    def exit_app(self):
        """Exit application safely"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.logger.info("Application closed by user")
            self.root.destroy()


def main():
    """Main entry point"""
    try:
        root = tk.Tk()
        app = TrafficControlGUI(root)
        root.mainloop()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        messagebox.showerror("Fatal Error", f"Application encountered a fatal error: {e}")


if __name__ == "__main__":
    main()
