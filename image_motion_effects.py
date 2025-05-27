import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading

class ImageMotionEffectsCV:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Motion Effects Studio (OpenCV)")
        self.root.geometry("600x400")
        
        # Variables
        self.image_var = tk.StringVar()
        self.effect_var = tk.StringVar()
        self.duration_var = tk.DoubleVar(value=5.0)
        self.fps_var = tk.IntVar(value=24)
        self.processing = False
        
        # Available effects
        self.effects = [
            "Zoom In",
            "Zoom Out",
            "Fade In",
            "Fade Out",
            "Slide In from Left",
            "Slide In from Right",
            "Pan Left to Right",
            "Pan Right to Left",
            "Ken Burns Effect"
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Image selection
        ttk.Label(main_frame, text="Image:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="Browse...", command=self.load_image).grid(row=0, column=1, sticky=tk.W, padx=5)
        image_entry = ttk.Entry(main_frame, textvariable=self.image_var, state="readonly")
        image_entry.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Effect selection
        ttk.Label(main_frame, text="Effect:").grid(row=2, column=0, sticky=tk.W, pady=5)
        effect_combo = ttk.Combobox(main_frame, textvariable=self.effect_var, 
                                   values=self.effects, state="readonly", width=30)
        effect_combo.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        effect_combo.set(self.effects[0])
        
        # Duration setting
        ttk.Label(main_frame, text="Duration (seconds):").grid(row=3, column=0, sticky=tk.W, pady=5)
        duration_scale = ttk.Scale(main_frame, from_=1.0, to=30.0, 
                                  variable=self.duration_var, orient=tk.HORIZONTAL)
        duration_scale.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        duration_label = ttk.Label(main_frame, text="5.0")
        duration_label.grid(row=3, column=2, padx=5)
        
        # Update duration label
        def update_duration_label(value):
            duration_label.config(text=f"{float(value):.1f}")
        duration_scale.config(command=update_duration_label)
        
        # FPS setting
        ttk.Label(main_frame, text="FPS:").grid(row=4, column=0, sticky=tk.W, pady=5)
        fps_frame = ttk.Frame(main_frame)
        fps_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        for fps in [24, 30, 60]:
            ttk.Radiobutton(fps_frame, text=str(fps), variable=self.fps_var, 
                           value=fps).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        self.apply_btn = ttk.Button(button_frame, text="Apply Effect", 
                                   command=self.apply_effect_threaded)
        self.apply_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
    def load_image(self):
        filepath = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("All Files", "*.*")
            ]
        )
        if filepath:
            self.image_var.set(filepath)
            self.status_label.config(text=f"Loaded: {os.path.basename(filepath)}")
            
    def apply_effect_threaded(self):
        if not self.image_var.get():
            messagebox.showwarning("No Image", "Please select an image first.")
            return
            
        if self.processing:
            messagebox.showinfo("Processing", "Another effect is being processed.")
            return
            
        # Run in separate thread to prevent UI freezing
        thread = threading.Thread(target=self.apply_effect)
        thread.daemon = True
        thread.start()
        
    def apply_effect(self):
        self.processing = True
        self.apply_btn.config(state="disabled")
        self.progress_var.set(0)
        
        image_path = self.image_var.get()
        effect = self.effect_var.get()
        duration = self.duration_var.get()
        fps = self.fps_var.get()
        
        try:
            self.status_label.config(text="Loading image...")
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise Exception("Failed to load image")
            
            height, width = img.shape[:2]
            
            # Generate output filename
            directory, filename = os.path.split(image_path)
            name, _ = os.path.splitext(filename)
            safe_effect_name = effect.replace(' ', '_').replace('/', '-')
            output_path = os.path.join(directory, f"{name}_{safe_effect_name}.mp4")
            
            # Ensure unique filename
            counter = 1
            while os.path.exists(output_path):
                output_path = os.path.join(directory, f"{name}_{safe_effect_name}_{counter}.mp4")
                counter += 1
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            total_frames = int(fps * duration)
            
            self.status_label.config(text=f"Applying {effect}...")
            
            for i in range(total_frames):
                t = i / total_frames  # Progress from 0 to 1
                
                if effect == "Zoom In":
                    scale = 1 + 0.5 * t
                    frame = self.zoom_image(img, scale)
                elif effect == "Zoom Out":
                    scale = 1.5 - 0.5 * t
                    frame = self.zoom_image(img, scale)
                elif effect == "Fade In":
                    alpha = t if i < fps else 1.0
                    frame = (img * alpha).astype(np.uint8)
                elif effect == "Fade Out":
                    alpha = 1.0 if i < total_frames - fps else (total_frames - i) / fps
                    frame = (img * alpha).astype(np.uint8)
                elif effect == "Slide In from Left":
                    x_offset = int(-width + width * t)
                    frame = self.translate_image(img, x_offset, 0)
                elif effect == "Slide In from Right":
                    x_offset = int(width - width * t)
                    frame = self.translate_image(img, x_offset, 0)
                elif effect == "Pan Left to Right":
                    scale = 1.2
                    zoomed = self.zoom_image(img, scale)
                    x_offset = int(-0.1 * width + 0.2 * width * t)
                    frame = self.translate_image(zoomed, x_offset, 0)
                elif effect == "Pan Right to Left":
                    scale = 1.2
                    zoomed = self.zoom_image(img, scale)
                    x_offset = int(0.1 * width - 0.2 * width * t)
                    frame = self.translate_image(zoomed, x_offset, 0)
                elif effect == "Ken Burns Effect":
                    scale = 1 + 0.3 * t
                    x_offset = int(0.05 * width * t)
                    y_offset = int(0.05 * height * t)
                    zoomed = self.zoom_image(img, scale)
                    frame = self.translate_image(zoomed, x_offset, y_offset)
                else:
                    frame = img
                
                # Ensure frame has correct dimensions
                if frame.shape[:2] != (height, width):
                    frame = cv2.resize(frame, (width, height))
                
                out.write(frame)
                
                # Update progress
                progress = (i + 1) / total_frames * 100
                self.progress_var.set(progress)
            
            out.release()
            
            self.progress_var.set(100)
            self.status_label.config(text=f"Success! Saved to: {os.path.basename(output_path)}")
            
            # Ask if user wants to open the file location
            if messagebox.askyesno("Success", f"Video saved successfully!\n\nOpen file location?"):
                if os.name == 'nt':  # Windows
                    os.startfile(directory)
                elif os.name == 'posix':  # macOS and Linux
                    os.system(f'open "{directory}"')
                    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Error occurred")
        finally:
            self.processing = False
            self.apply_btn.config(state="normal")
            self.progress_var.set(0)
    
    def zoom_image(self, img, scale):
        height, width = img.shape[:2]
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Resize image
        resized = cv2.resize(img, (new_width, new_height))
        
        # Crop to original size (center crop)
        x_start = (new_width - width) // 2
        y_start = (new_height - height) // 2
        
        if scale > 1:
            return resized[y_start:y_start+height, x_start:x_start+width]
        else:
            # Pad if scale < 1
            result = np.zeros_like(img)
            x_offset = (width - new_width) // 2
            y_offset = (height - new_height) // 2
            result[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized
            return result
    
    def translate_image(self, img, x_offset, y_offset):
        height, width = img.shape[:2]
        M = np.float32([[1, 0, x_offset], [0, 1, y_offset]])
        return cv2.warpAffine(img, M, (width, height))

if __name__ == "__main__":
    # First install opencv if not installed
    try:
        import cv2
    except ImportError:
        print("OpenCV not installed. Please run: pip install opencv-python")
        exit(1)
    
    root = tk.Tk()
    app = ImageMotionEffectsCV(root)
    root.mainloop()