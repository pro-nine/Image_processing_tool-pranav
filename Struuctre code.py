import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.configure(background='white')  # Set background color

        # Initialize webcam
        self.webcam = cv2.VideoCapture(0)

        # Create label for camera frame
        self.camera_label = tk.Label(window, text="Camera Frame", font=("Arial", 12), bg='#F1FFFC')
        self.camera_label.grid(row=0, column=0, padx=10, pady=5)

        # Create canvas to display camera frame
        self.camera_canvas = tk.Canvas(window, width=640, height=480, bg='#d7f4ff', highlightthickness=2, highlightbackground='#071B24')  # Set canvas background and border color
        self.camera_canvas.grid(row=1, column=0, padx=10, pady=5)

        # Create label for captured image frame
        self.captured_label = tk.Label(window, text="Captured Image", font=("Arial", 12), bg='#F1FFFC')  # Set label background color
        self.captured_label.grid(row=0, column=1, padx=10, pady=5)

        # Create canvas to display captured image
        self.captured_canvas = tk.Canvas(window, width=640, height=480, bg='#d7f4ff', highlightthickness=2, highlightbackground='#071B24')  # Set canvas background and border color
        self.captured_canvas.grid(row=1, column=1, padx=10, pady=5)

        # Frame to hold buttons
        self.controls_frame = tk.Frame(window, bg='#F1FFFC')  # Set frame background color
        self.controls_frame.grid(row=2, columnspan=2, pady=20)

        # Capture button
        self.capture_button = tk.Button(self.controls_frame, text="Capture Image", command=self.capture_image, bg='#9B3922', fg='white', bd=0, relief=tk.FLAT, font=("Helvetica", 14))  # Set button background, foreground, border color and style
        self.capture_button.grid(row=0, column=0, padx=20, pady=5)

        # Save button
        self.save_button = tk.Button(self.controls_frame, text="Save Image", command=self.save_image, bg='#9B3922', fg='white', bd=0, relief=tk.FLAT, font=("Helvetica", 14))  # Set button background, foreground, border color and style
        self.save_button.grid(row=0, column=1, padx=20, pady=5)

        # Exit button
        self.exit_button = tk.Button(self.controls_frame, text="Exit", command=self.window.quit, bg='#9B3922', fg='white', bd=0, relief=tk.FLAT, font=("Helvetica", 14))  # Set button background, foreground, border color and style
        self.exit_button.grid(row=0, column=2, padx=20, pady=5)

        # Counter for image filenames
        self.image_counter = 1

        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.webcam.read()
        if ret:
            self.camera_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.camera_photo = ImageTk.PhotoImage(image=Image.fromarray(self.camera_frame))
            self.camera_canvas.create_image(0, 0, image=self.camera_photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def capture_image(self):
        self.captured_frame = self.camera_frame.copy()  # Store the captured frame
        self.display_captured_image(self.captured_frame)
        self.image_counter += 1

    def display_captured_image(self, image):
        # Resize the image to fit within the canvas while maintaining aspect ratio
        img = Image.fromarray(image)
        img.thumbnail((self.captured_canvas.winfo_width(), self.captured_canvas.winfo_height()))
        captured_photo = ImageTk.PhotoImage(image=img)
        self.captured_canvas.create_image(0, 0, image=captured_photo, anchor=tk.NW)
        self.captured_canvas.image = captured_photo  # Keep a reference to avoid garbage collection

    def save_image(self):
        filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")], initialfile="ProjectdataIMG{}.jpg".format(self.image_counter))
        if filename:
            cv2.imwrite(filename, cv2.cvtColor(self.captured_frame, cv2.COLOR_RGB2BGR))
            print("Image saved as", filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root, "Webcam Application")
