import cv2
import numpy as np
from gstreamer.gstreamer_base_code import __gstreamer_pipeline
from stereo_rectification_calibrated import stereo_rectification_calibrated
from stereo_rectification_uncalibrated import stereo_rectification_uncalibrated
import matplotlib.pyplot as plt
print(cv2.__version__)

def undistort_only(leftFrame, rightFrame):
    fs = cv2.FileStorage("calibration_params.yml", cv2.FILE_STORAGE_READ)
    calibParams = {'cameraMatrixLeft' : fs.getNode("cameraMatrixLeft").mat(), 
                   'distCoeffsLeft' : fs.getNode("distCoeffsLeft").mat(), 
                    'cameraMatrixRight' : fs.getNode("cameraMatrixRight").mat(), 
                    'distCoeffsRight' : fs.getNode("distCoeffsRight").mat(), 
                    'R' : fs.getNode("R").mat(), 
                    'T' : fs.getNode("T").mat() }
   
    h, w = leftFrame.shape[:2]
    newcameramtx_left, roi = cv2.getOptimalNewCameraMatrix(calibParams["cameraMatrixLeft"], calibParams["distCoeffsLeft"], (w,h), 1, (w,h))
    dst_left = cv2.undistort(leftFrame, calibParams["cameraMatrixLeft"], calibParams["distCoeffsLeft"], None, newcameramtx_left)

    h, w = rightFrame.shape[:2]
    newcameramtx_right, roi = cv2.getOptimalNewCameraMatrix(calibParams["cameraMatrixRight"], calibParams["distCoeffsRight"], (w,h), 1, (w,h))
    dst_right = cv2.undistort(rightFrame, calibParams["cameraMatrixRight"], calibParams["distCoeffsRight"], None, newcameramtx_right)

    return dst_left, dst_right


#initialise video capture object   
cam1 = cv2.VideoCapture(__gstreamer_pipeline(camera_id=1, flip_method=0), cv2.CAP_GSTREAMER)
cam2 = cv2.VideoCapture(__gstreamer_pipeline(camera_id=0, flip_method=0), cv2.CAP_GSTREAMER)

#check if video capture object was properly initialised and able to open
if not cam1.isOpened():
 print("Cannot open camera 1")
 exit()

if not cam2.isOpened():
 print("Cannot open camera 2")
 exit()

#read 2 images in order ot get dimensions and compute first homography matrix
img1 = cv2.imread("img_data/left_image_1.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("img_data/right_image_1.jpg", cv2.IMREAD_GRAYSCALE)

#Main loop
h1, w1 = img1.shape
h2, w2 = img2.shape
H1, H2 = stereo_rectification_uncalibrated(img1, img2)

#get rectification maps
maps_left_cam, maps_right_cam = stereo_rectification_calibrated()

while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    #left_frame_rectified, right_frame_rectified = stereo_rectification_calibrated(frame1, frame2)
    #left_frame_rectified, right_frame_rectified = undistort_only(frame1, frame2)

    #left_frame_rectified = cv2.warpPerspective(frame1, H1, (w1, h1))
    #right_frame_rectified = cv2.warpPerspective(frame2, H2, (w2, h2))

    left_frame_rectified = cv2.remap(frame1, maps_left_cam[0], maps_left_cam[1], cv2.INTER_LANCZOS4)
    right_frame_rectified = cv2.remap(frame2, maps_right_cam[0], maps_right_cam[1], cv2.INTER_LANCZOS4)

    cv2.imshow('LEFT FRAME',frame1)
    cv2.imshow('RIGHT FRAME', frame2)
    cv2.imshow('LEFT FRAME UDIST',left_frame_rectified)
    cv2.imshow('RIGHT FRAME UDIST', right_frame_rectified)
    cv2.moveWindow('LEFT FRAME', 100, 250)
    cv2.moveWindow('RIGHT FRAME', 1100, 250)
    cv2.moveWindow('LEFT FRAME UDIST', 100, 850)
    cv2.moveWindow('RIGHT FRAME UDIST', 1100, 850)
     
    if cv2.waitKey(1)==ord('q'):
        break

#close video capture object and close opencv window   
cam1.release()
cam2.release()
cv2.destroyAllWindows()