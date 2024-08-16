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

        # Initialize webcam
        self.webcam = cv2.VideoCapture(0)

        # camera label
        self.camera_label = tk.Label(window, text="Camera Frame", font=("Arial", 12))
        self.camera_label.place(x=50, y=100)

        # Create canvas to display camera frame
        self.camera_canvas = tk.Canvas(window, width=640, height=480)
        self.camera_canvas.pack(side=tk.LEFT)

        # Create label for captured image frame
        self.captured_label = tk.Label(window, text="Captured Image", font=("Arial", 12))
        self.captured_label.place(x=1150, y=100)

        # Create canvas to display captured image
        self.captured_canvas = tk.Canvas(window, width=640, height=480)
        self.captured_canvas.pack(side=tk.RIGHT)

        # Exit button
        self.exit_button = tk.Button(window, text="Exit", command=self.window.quit)
        self.exit_button.pack(side=tk.BOTTOM, pady=5)
        # Save button
        self.save_button = tk.Button(window, text="Save Image", command=self.save_image)
        self.save_button.pack(side=tk.BOTTOM, pady=5)
        # RGB ratio label
        self.rgb_label = tk.Label(window, text="RGB Ratio:", font=("Arial", 12))
        self.rgb_label.pack(side=tk.BOTTOM, pady=5)
        # Capture button
        self.capture_button = tk.Button(window, text="Capture Image", command=self.capture_image)
        self.capture_button.pack(side=tk.BOTTOM, pady=10)

        # Dictionary to store RGB values for each image
        self.rgb_values = {}

        # Load existing RGB data from CSV
        self.load_rgb_data()

        # Counter for image filenames
        self.image_counter = len(self.rgb_values) + 1

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
        self.calculate_rgb_ratio(self.captured_frame)

    def display_captured_image(self, image):
        # Resize the image to fit within the canvas while maintaining aspect ratio
        img = Image.fromarray(image)
        img.thumbnail((self.captured_canvas.winfo_width(), self.captured_canvas.winfo_height()))
        captured_photo = ImageTk.PhotoImage(image=img)
        self.captured_canvas.create_image(0, 0, image=captured_photo, anchor=tk.NW)
        self.captured_canvas.image = captured_photo  # Keep a reference to avoid garbage collection

    def calculate_rgb_ratio(self, image):
        r = np.mean(image[:, :, 0])
        g = np.mean(image[:, :, 1])
        b = np.mean(image[:, :, 2])
        total = r + g + b
        if total != 0:
            r_ratio = r / total
            g_ratio = g / total
            b_ratio = b / total
            self.rgb_label.config(text="RGB Ratio: R={:.2f}, G={:.2f}, B={:.2f}".format(r_ratio, g_ratio, b_ratio))

            # Store RGB values for the captured image
            self.rgb_values["ProjectdataIMG{}.jpg".format(self.image_counter)] = (r_ratio, g_ratio, b_ratio)
        else:
            self.rgb_label.config(text="Error: Total intensity is zero!")

    def save_image(self):
        filename = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")],
                                                initialfile="ProjectdataIMG{}.jpg".format(self.image_counter))
        if filename:
            cv2.imwrite(filename, cv2.cvtColor(self.captured_frame, cv2.COLOR_RGB2BGR))
            print("Image saved as", filename)

            # Save RGB values to a CSV file
            with open("rgb_data.csv", "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Image Name", "R", "G", "B"])
                for image_name, rgb_values in self.rgb_values.items():
                    writer.writerow([image_name, rgb_values[0], rgb_values[1], rgb_values[2]])
                print("RGB values saved to csv file.")

            # Increment image counter
            self.image_counter += 1

    def load_rgb_data(self):
        try:
            with open("rgb_data.csv", "r", newline='') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                for row in reader:
                    self.rgb_values[row[0]] = (float(row[1]), float(row[2]), float(row[3]))
            print("RGB data loaded successfully.")
        except FileNotFoundError:
            print("No existing RGB data found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root, "RGB Image Capture")
