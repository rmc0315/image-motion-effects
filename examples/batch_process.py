#!/usr/bin/env python3
"""
batch_process.py - Batch processing example for Image Motion Effects

This script demonstrates how to apply effects to multiple images at once,
perfect for creating a series of motion graphics for your YouTube videos.
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path
import argparse
import time

# Add parent directory to path to import the main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class BatchProcessor:
    def __init__(self):
        self.effects = {
            "zoom_in": self.zoom_in_effect,
            "zoom_out": self.zoom_out_effect,
            "ken_burns": self.ken_burns_effect,
            "fade_in": self.fade_in_effect,
            "slide_left": self.slide_from_left_effect,
            "pan_right": self.pan_right_effect
        }
    
    def process_folder(self, input_folder, output_folder, effect="ken_burns", 
                      duration=5.0, fps=30, prefix=""):
        """Process all images in a folder with the specified effect."""
        
        # Create output folder if it doesn't exist
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        
        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(Path(input_folder).glob(f'*{ext}'))
            image_files.extend(Path(input_folder).glob(f'*{ext.upper()}'))
        
        print(f"Found {len(image_files)} images to process")
        
        # Process each image
        for idx, image_path in enumerate(image_files):
            print(f"\nProcessing {idx + 1}/{len(image_files)}: {image_path.name}")
            
            # Load image
            img = cv2.imread(str(image_path))
            if img is None:
                print(f"Failed to load {image_path.name}, skipping...")
                continue
            
            # Generate output filename
            output_name = f"{prefix}{image_path.stem}_{effect}.mp4"
            output_path = Path(output_folder) / output_name
            
            # Apply effect
            try:
                self.apply_effect(img, str(output_path), effect, duration, fps)
                print(f"✓ Saved: {output_name}")
            except Exception as e:
                print(f"✗ Error processing {image_path.name}: {e}")
    
    def apply_effect(self, img, output_path, effect_name, duration, fps):
        """Apply the specified effect to an image and save as video."""
        
        height, width = img.shape[:2]
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        total_frames = int(fps * duration)
        
        # Get effect function
        effect_func = self.effects.get(effect_name, self.ken_burns_effect)
        
        # Generate frames
        for i in range(total_frames):
            t = i / total_frames  # Progress from 0 to 1
            frame = effect_func(img, t, width, height)
            
            # Ensure correct dimensions
            if frame.shape[:2] != (height, width):
                frame = cv2.resize(frame, (width, height))
            
            out.write(frame)
        
        out.release()
    
    # Effect implementations
    def zoom_in_effect(self, img, t, width, height):
        scale = 1 + 0.5 * t
        return self._zoom_image(img, scale)
    
    def zoom_out_effect(self, img, t, width, height):
        scale = 1.5 - 0.5 * t
        return self._zoom_image(img, scale)
    
    def ken_burns_effect(self, img, t, width, height):
        scale = 1 + 0.3 * t
        x_offset = int(0.05 * width * t)
        y_offset = int(0.05 * height * t)
        zoomed = self._zoom_image(img, scale)
        return self._translate_image(zoomed, x_offset, y_offset)
    
    def fade_in_effect(self, img, t, width, height):
        alpha = t
        return (img * alpha).astype(np.uint8)
    
    def slide_from_left_effect(self, img, t, width, height):
        x_offset = int(-width + width * t)
        return self._translate_image(img, x_offset, 0)
    
    def pan_right_effect(self, img, t, width, height):
        scale = 1.2
        zoomed = self._zoom_image(img, scale)
        x_offset = int(0.1 * width - 0.2 * width * t)
        return self._translate_image(zoomed, x_offset, 0)
    
    # Helper methods
    def _zoom_image(self, img, scale):
        height, width = img.shape[:2]
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        resized = cv2.resize(img, (new_width, new_height))
        
        x_start = (new_width - width) // 2
        y_start = (new_height - height) // 2
        
        if scale > 1:
            return resized[y_start:y_start+height, x_start:x_start+width]
        else:
            result = np.zeros_like(img)
            x_offset = (width - new_width) // 2
            y_offset = (height - new_height) // 2
            result[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized
            return result
    
    def _translate_image(self, img, x_offset, y_offset):
        height, width = img.shape[:2]
        M = np.float32([[1, 0, x_offset], [0, 1, y_offset]])
        return cv2.warpAffine(img, M, (width, height))


def main():
    parser = argparse.ArgumentParser(
        description='Batch process images with motion effects for YouTube videos'
    )
    parser.add_argument('input_folder', help='Folder containing input images')
    parser.add_argument('output_folder', help='Folder for output videos')
    parser.add_argument('--effect', '-e', default='ken_burns',
                      choices=['zoom_in', 'zoom_out', 'ken_burns', 'fade_in', 
                              'slide_left', 'pan_right'],
                      help='Effect to apply (default: ken_burns)')
    parser.add_argument('--duration', '-d', type=float, default=5.0,
                      help='Duration in seconds (default: 5.0)')
    parser.add_argument('--fps', '-f', type=int, default=30,
                      choices=[24, 30, 60],
                      help='Frames per second (default: 30)')
    parser.add_argument('--prefix', '-p', default='',
                      help='Prefix for output filenames')
    
    args = parser.parse_args()
    
    # Check if input folder exists
    if not os.path.exists(args.input_folder):
        print(f"Error: Input folder '{args.input_folder}' does not exist")
        return
    
    # Start processing
    print(f"Starting batch processing...")
    print(f"Effect: {args.effect}")
    print(f"Duration: {args.duration}s")
    print(f"FPS: {args.fps}")
    print("-" * 50)
    
    start_time = time.time()
    
    processor = BatchProcessor()
    processor.process_folder(
        args.input_folder,
        args.output_folder,
        args.effect,
        args.duration,
        args.fps,
        args.prefix
    )
    
    elapsed_time = time.time() - start_time
    print(f"\nBatch processing complete in {elapsed_time:.1f} seconds")


if __name__ == "__main__":
    main()