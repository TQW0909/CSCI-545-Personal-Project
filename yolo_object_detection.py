from ultralytics import YOLO
import cv2
import os

images_dir = "images"

if not os.path.exists(images_dir):
    print(f"Error: Directory '{images_dir}' does not exist.")
    exit(1)

# Load images using OpenCV
images = []
for image in os.listdir(images_dir):
    img_path = os.path.join(images_dir, image)
    img = cv2.imread(img_path)
    if img is not None:
        images.append(img)


# Load the YOLOv11s model
model = YOLO('yolov10s.pt')

results = model(images)

# Process results list
for i, result in enumerate(results):
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    # keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename=f"result{i}.jpg")  # save to disk
