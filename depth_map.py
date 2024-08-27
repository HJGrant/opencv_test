import cv2
import numpy as np


def depth_map(img1, img2):
    block_size = 8
    min_disp = -128
    max_disp = 128

    num_disp = max_disp - min_disp

    uniquenessRatio = 3

    speckleWindowSize = 75

    speckleRange = 75
    disp12MaxDiff = 0

    stereo = cv2.StereoSGBM_create(
       minDisparity=min_disp,
       numDisparities=num_disp,
       blockSize=block_size,
       uniquenessRatio=uniquenessRatio,
       speckleWindowSize=speckleWindowSize,
       speckleRange=speckleRange,
       disp12MaxDiff=disp12MaxDiff,
       P1=98 * 1 * block_size * block_size, 
       P2=120 * 1 * block_size * block_size
    )   

    disparity_SGBM = stereo.compute(img1, img2) 
    disparity_SGBM = cv2.normalize(disparity_SGBM, disparity_SGBM, alpha=255, beta=0, norm_type=cv2.NORM_MINMAX)
    disparity_SGBM = np.uint8(disparity_SGBM)

    return disparity_SGBM