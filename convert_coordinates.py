import numpy as np
from scipy.spatial.transform import Rotation as R

base_orientation = [0, 0, 0]  # No rotation

# Camera orientation
roll = float(input("Enter roll of camera (in degrees): "))
pitch = float(input("Enter pitch of camera (in degrees): "))
yaw = float(input("Enter yaw of camera (in degrees): "))

camera_orientation = [roll, pitch, yaw]  # [roll, pitch, yaw] in degrees

x = float(input("Enter x coordinate of camera (in m): "))
y = float(input("Enter y coordinate of camera (in m): "))
z = float(input("Enter z coordinate of camera (in m): "))

# Translation vector 
T = [x, y, z] 

X = float(input("Enter object x coordinate in camera frame (in m): "))
Y = float(input("Enter object y coordinate in camera frame (in m): "))
Z = float(input("Enter object z coordinate in camera frame (in m): "))

# Define object position in camera frame
P_camera = [X, Y, Z] 


# Assuming base and camera orientations are given as [roll, pitch, yaw]
base_rot = R.from_euler('xyz', base_orientation, degrees=True)
camera_rot = R.from_euler('xyz', camera_orientation, degrees=True)

# Convert to rotation matrices
R_base = base_rot.as_matrix()
R_camera = camera_rot.as_matrix()

# Compute relative rotation: R_base_camera = R_base.T * R_camera
R_base_camera = R_base.T @ R_camera

# Transforms a point from the camera frame to the base frame.
R_matrix = np.array(R_base_camera).reshape((3, 3))
T = np.array(T).reshape((3, 1))
P_camera = np.array(P_camera).reshape((3, 1))

P_base = (R_matrix @ P_camera + T).flatten()

# Display results
print("\n--- Rotation Matrix from Camera to Base Frame (R_base_camera) ---")
print(R_base_camera)

print("\n--- Object Position in Robot Base Frame ---")
print(f"X: {P_base[0]:.4f}")
print(f"Y: {P_base[1]:.4f}")
print(f"Z: {P_base[2]:.4f}")