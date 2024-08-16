import cv2
import numpy as np

# Read the input image
image = cv2.imread('Project_imgPROCESSING_img.jpeg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Perform Gaussian blurring to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Hough Circle Transform for circle detection
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                            param1=200, param2=30, minRadius=10, maxRadius=100)

# Dictionary mapping circle indices to their names
circle_names = {0: "Circle 1", 1: "Circle 2", 2: "Circle 3", 3: "Circle 4", 4: "Circle 5", 5: "Circle 6", 6: "Circle 7"}  # Add more names as needed

# If circles are detected
if circles is not None:
    # Convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    
    # Loop over the detected circles
    for i, (x, y, r) in enumerate(circles):
        # Extract the circular region as ROI
        roi = image[y - r:y + r, x - r:x + r]
        
        # Calculate the average color (RGB values) within the ROI
        avg_color = np.mean(roi, axis=(0, 1)).astype(int)
        
        # Calculate the color strength (e.g., sum of RGB values)
        color_strength = np.sum(avg_color)
        
        # Print the name, average color, and color strength
        name = circle_names.get(i, "Unknown")
        print(f"Circle Name: {name}")
        print("Average Color (RGB):", avg_color)
        print("Color Strength:", color_strength)
        
        # Draw the circle and bounding box
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)
        cv2.putText(image, name, (x - 50, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the output image
cv2.imshow('Detected Circles', image)
cv2.waitKey(0)
cv2.destroyAllWindows()