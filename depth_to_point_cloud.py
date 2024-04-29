import cv2
import numpy as np
import os

def generate_point_cloud(depth_image, camera_intrinsics):
    # Get image dimensions
    print(depth_image.shape)
    height, width, _ = depth_image.shape

    # Get camera intrinsic parameters
    fx, fy, cx, cy = camera_intrinsics

    # Generate grid of pixel coordinates
    u, v = np.meshgrid(np.arange(width), np.arange(height))
    
    print(u.shape)
     # Convert pixel coordinates to 3D coordinates
    x = (u - cx) * depth_image / fx
    y = (v - cy) * depth_image / fy
    z = depth_image

    # Stack 3D coordinates to form point cloud
    point_cloud = np.stack((x, y, z), axis=-1)

    return point_cloud

# Load depth image
depth_image = cv2.imread(os.path.join(os.getcwd(), 'depth_img.png'), cv2.IMREAD_UNCHANGED).astype(np.float32)

# Camera intrinsics (fx, fy, cx, cy)
camera_intrinsics = (520.9, 521.0, 325.1, 249.7)  # Example intrinsics (replace with actual values)

# Generate point cloud
point_cloud = generate_point_cloud(depth_image, camera_intrinsics)

# Visualize point cloud (optional)
# For visualization, you can use libraries like Matplotlib, Open3D, or others.

# Save point cloud (optional)
# You can save the generated point cloud to a file for further processing or visualization.
