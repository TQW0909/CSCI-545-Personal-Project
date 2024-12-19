import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Read a single frame from the webcam
ret, frame = cap.read()

if ret:
    # Save the captured image to a file
    image_path = "captured_image.png"
    cv2.imwrite(image_path, frame)
    print(f"Image saved successfully at {image_path}")
else:
    print("Error: Could not read frame from webcam.")

# Release the webcam
cap.release()