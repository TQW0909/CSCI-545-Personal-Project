
import cv2

# Load the captured image
image_path = "captured_image.png"
image = cv2.imread(image_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray_image, 100, 200)

# Display the original and processed images
cv2.imshow("Original Image", image)
cv2.imshow("Grayscale Image", gray_image)
cv2.imshow("Edges Detected", edges)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
