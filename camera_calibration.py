import cv2
import numpy as np
import glob

chessboard_size = (8, 6)  # Number of inner corners per chessboard row and column
square_size = 25  # mm 

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0), ....,(8,5,8)
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp = objp * square_size

# Arrays to store object points and image points from all the images
objpoints = []  # 3d points in real-world space
imgpoints = []  # 2d points in image plane

# Load all images from the calibration_images folder
images = glob.glob('calibration_images/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    # If found, add object points and image points (after refining them)
    if ret:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), 
                                    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
        cv2.imshow('Chessboard Corners', img)
        cv2.waitKey(100)

cv2.destroyAllWindows()

# Calibrate the camera
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Camera matrix:")
print(camera_matrix)
print("\nDistortion coefficients:")
print(dist_coeffs)

# Saving the calibration results for future use
np.savez("calibration_data.npz", camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)


# Calculate the re-projection error
total_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], camera_matrix, dist_coeffs)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    total_error += error

mean_error = total_error / len(objpoints)
print(f"Total re-projection error: {mean_error}")




# img = cv2.imread('calibration_images/your_image.jpg')
# h, w = img.shape[:2]
# new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))

# # Undistort
# dst = cv2.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix)

# # Crop the image (if needed)
# x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]

# # Display the original and undistorted images
# cv2.imshow("Original Image", img)
# cv2.imshow("Undistorted Image", dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
