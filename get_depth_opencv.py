import os
from PIL import Image  # Assuming you're using PIL for image processing
import cv2
import numpy as np
from gstreamer.gstreamer_base_code import __gstreamer_pipeline
from stereo_rectification_calibrated import stereo_rectification_calibrated
from stereo_rectification_uncalibrated import stereo_rectification_uncalibrated
from undistort_only import undistort_only
from depth_map import depth_map
import matplotlib.pyplot as plt

def process_image_pair(left_image_path, right_image_path, save_path):
    """
    Perform your desired action on the image pair.
    This function receives the paths of the left and right images.
    """
    left_image = cv2.imread(left_image_path)
    right_image = cv2.imread(right_image_path)

    left_frame_rectified = cv2.remap(left_image, maps_left_cam[0], maps_left_cam[1], cv2.INTER_LANCZOS4)
    right_frame_rectified = cv2.remap(right_image, maps_right_cam[0], maps_right_cam[1], cv2.INTER_LANCZOS4)

    disparity = depth_map(left_frame_rectified, right_frame_rectified)

    filtered_disparity = cv2.bilateralFilter(disparity, d=3, sigmaColor=150, sigmaSpace=125)
    filtered_disparity = filtered_disparity.astype(np.uint16) 

    cv2.imwrite(save_path, filtered_disparity)
    print(f"Saved: {save_path}")

def main():
    left_folder = 'data/aruco/output_aruco_src_1'
    right_folder = 'data/aruco/output_aruco_src_0'
    depth_folder = 'data/aruco/depth'

    # Create the depth folder if it doesn't exist
    os.makedirs(depth_folder, exist_ok=True)

    # Get a list of images in both folders
    left_images = sorted(os.listdir(left_folder))
    right_images = sorted(os.listdir(right_folder))

    for left_image_name in left_images:
        left_image_path = os.path.join(left_folder, left_image_name)
        right_image_path = os.path.join(right_folder, left_image_name)

        # Check if corresponding right image exists
        if os.path.exists(right_image_path):
            save_path = os.path.join(depth_folder, left_image_name)
            process_image_pair(left_image_path, right_image_path, save_path)
        else:
            print(f"Right image for {left_image_name} not found")

if __name__ == "__main__":
    maps_left_cam, maps_right_cam, ROI1, ROI2 = stereo_rectification_calibrated()

    main()