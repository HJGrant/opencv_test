import cv2
import numpy as np
from depth_map import depth_map
from vpi_depth_map import vpi_stereo

global img_right
global img_left

global min_disp 
global num_disp
global block_size
global disp12MaxDiff
global uniquenessRatio
global speckleWindowSize
global speckleRange


def depth_map(img1, img2):
    min_disp = 0         #original 16
    num_disp = 200       #original 64
    block_size = 7             #original 8
    disp12MaxDiff = 50         #original 1
    uniquenessRatio = 0      #original 10
    speckleWindowSize = 100     #original 10
    speckleRange = 8          #original 8
    preFilterCap = 3

    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=block_size,
        uniquenessRatio=uniquenessRatio,
        speckleWindowSize=speckleWindowSize,
        speckleRange=speckleRange,
        disp12MaxDiff=disp12MaxDiff,
        P1=8 * 1 * block_size * block_size, 
        P2=32 * 1 * block_size * block_size
    )   

    disparity_SGBM = stereo.compute(img1, img2) 
    disparity_SGBM = cv2.normalize(disparity_SGBM, disparity_SGBM, alpha=255, beta=0, norm_type=cv2.NORM_MINMAX)
    disparity_SGBM = np.uint8(disparity_SGBM)

    return disparity_SGBM

def on_trackbar(min_disp, num_disp, block_size, disp12MaxDiff, uniquenessRatio, speckleWindowSize, speckleRange):

    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=block_size,
        uniquenessRatio=uniquenessRatio,
        speckleWindowSize=speckleWindowSize,
        speckleRange=speckleRange,
        disp12MaxDiff=disp12MaxDiff,
        P1=8 * 1 * block_size * block_size, 
        P2=32 * 1 * block_size * block_size
    )   

    disparity_SGBM = stereo.compute(img_left, img_right) 
    disparity_SGBM = cv2.normalize(disparity_SGBM, disparity_SGBM, alpha=255, beta=0, norm_type=cv2.NORM_MINMAX)
    disparity_SGBM = np.uint8(disparity_SGBM)


    cv2.imshow('DISPARITY', disparity_SGBM)
    pass

img_left = cv2.imread("left.png")
img_right = cv2.imread("right.png")

img_left = cv2.resize(img_left, (960,540))
img_right = cv2.resize(img_right, (960,540))

#disparity = depth_map(img_left, img_right)
disparity = vpi_stereo(img_left, img_right)

cv2.imshow('LEFT', img_left)
cv2.imshow('DISPARITY', disparity)

cv2.moveWindow('DISPARITY', 1250, 0)

cv2.imwrite("output_disparity_map_1_frame.png", disparity)

cv2.waitKey()
cv2.destroyAllWindows()