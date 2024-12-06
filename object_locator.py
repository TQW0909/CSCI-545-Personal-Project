from ultralytics import YOLO
import cv2
import numpy as np
import argparse

# Command-line argument parser to select the mode
parser = argparse.ArgumentParser(description="Distance Calculation Modes: calibrate or use.")
parser.add_argument('--mode', type=str, choices=['calibrate', 'use'], required=True, help="Choose the mode: 'calibrate' or 'use'.")
args = parser.parse_args()

# Load calibration data
calibration_data = np.load("calibration_data.npz")
camera_matrix = calibration_data["camera_matrix"]
dist_coeffs = calibration_data["dist_coeffs"]

# Load the YOLO model
model = YOLO('yolov10s.pt')  # Adjust model name if needed

# Load the captured image
image_path = "captured_image.png"
image = cv2.imread(image_path)

# Undistort the image using the calibration data
h, w = image.shape[:2]
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)

# Crop the image (if needed, based on region of interest)
x, y, w, h = roi
undistorted_image = undistorted_image[y:y+h, x:x+w]

# Run the YOLO model on the undistorted image
results = model(undistorted_image)

# Define the class labels and specify the classes of interest
class_labels = model.names
target_classes = ["bottle", "can", "cup"]

# Load or define the distance calculation coefficient
distance_coefficient = None
if args.mode == 'use':
    try:
        coefficient_data = np.load("distance_coefficient.npz")
        distance_coefficient = coefficient_data["distance_coefficient"]
        print(f"Loaded distance calculation coefficient: {distance_coefficient}")
    except FileNotFoundError:
        print("Distance calculation coefficient not found. Please run in 'calibrate' mode first.")
        exit()

# Known dimensions and distance for calibration (in mm)
H_real = 106  # Known height of the object
W_real = 50   # Known width of the object
D_real = 400  # Known distance from camera to object

# Process results for each detected object
for i, result in enumerate(results):
    boxes = result.boxes

    for box in boxes:
        class_id = int(box.cls[0])
        class_name = class_labels[class_id]

        # Only process target classes (e.g., bottle, can, cup)
        if class_name in target_classes:
            # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Calculate the height and width of the object in the image in pixels
            H_image = y2 - y1
            W_image = x2 - x1

            # Debugging output for bounding box dimensions and apparent height/width
            print(f"Bounding box coordinates: (x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2})")
            print(f"Apparent height in image (H_image): {H_image} pixels")
            print(f"Apparent width in image (W_image): {W_image} pixels")

            # Mode: calibrate
            if args.mode == 'calibrate':
                # Calculate focal lengths based on known height and width
                f_height = (H_image * D_real) / H_real
                f_width = (W_image * D_real) / W_real

                # Average the focal lengths for height and width
                distance_coefficient = (f_height + f_width) / 2

                # Save the coefficient for future use
                np.savez("distance_coefficient.npz", distance_coefficient=distance_coefficient)
                print(f"Calculated and saved distance calculation coefficient: {distance_coefficient}")

                # Use the calculated coefficient to estimate distance
                Z_c = (H_real * distance_coefficient) / H_image
                print(f"Estimated distance from camera (Z_c): {Z_c:.2f} mm")

            # Mode: use
            elif args.mode == 'use':
                # Use the loaded or calculated coefficient to estimate the distance
                if distance_coefficient is not None:
                    Z_c = (H_real * distance_coefficient) / H_image
                    print(f"Estimated distance from camera (Z_c): {Z_c:.2f} mm")
                else:
                    print("Error: Distance coefficient is not available.")
                    exit()

            # Calculate the center of the bounding box (image coordinates)
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # Using the undistorted coordinates to calculate X_c and Y_c
            X_c = (center_x - camera_matrix[0, 2]) * Z_c / camera_matrix[0, 0]
            Y_c = (center_y - camera_matrix[1, 2]) * Z_c / camera_matrix[1, 1]

            # Store the coordinates of the object in the camera frame
            camera_coordinates = np.array([X_c, Y_c, Z_c])
            print(f"Camera frame coordinates for {class_name}: {camera_coordinates}")

            # Draw the bounding box for visualization
            cv2.rectangle(undistorted_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(undistorted_image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Draw a circle at the center for visualization
            cv2.circle(undistorted_image, (center_x, center_y), 5, (255, 0, 0), -1)
            print(f"Detected {class_name} center at: ({center_x}, {center_y})")

    # Save the filtered results for review
    cv2.imwrite(f"filtered_result_{i}.jpg", undistorted_image)

# Close the window
cv2.destroyAllWindows()
