import cv2
import numpy as np

def stereo_rectification_calibrated():
    #read the intrinsic parametres
    fs = cv2.FileStorage("calibration_params.yml", cv2.FILE_STORAGE_READ)
    calibParams = {'cameraMatrixLeft' : fs.getNode("cameraMatrixLeft").mat(), 
                   'distCoeffsLeft' : fs.getNode("distCoeffsLeft").mat(), 
                    'cameraMatrixRight' : fs.getNode("cameraMatrixRight").mat(), 
                    'distCoeffsRight' : fs.getNode("distCoeffsRight").mat(), 
                    'R' : fs.getNode("R").mat(), 
                    'T' : fs.getNode("T").mat() }
    

    #TODO: add getOptimalCameraMatrix

    #compute the extrinsic parameters from the intrinsic parameteres recieved from the calibration process
    #TODO: how to ge new ImageSize parameter ? 
    R1, R2, P1, P2, Q, ROI1, ROI2 = cv2.stereoRectify(calibParams['cameraMatrixLeft'], calibParams['distCoeffsLeft'], 
                                                    calibParams['cameraMatrixRight'], calibParams['distCoeffsRight'], 
                                                    (960, 540), calibParams['R'], calibParams['T'], 1, newImageSize=(960, 540) )
    
    #TODO: implement code to get undistortion and rectification transformation map
    maps_left_cam = []
    maps_right_cam = []
    maps_left_cam = cv2.initUndistortRectifyMap(calibParams['cameraMatrixLeft'], calibParams['distCoeffsLeft'], R1, P1, (1920, 1080), cv2.CV_16SC2)
    maps_right_cam = cv2.initUndistortRectifyMap(calibParams['cameraMatrixRight'], calibParams['distCoeffsRight'], R2, P2, (1920, 1080), cv2.CV_16SC2)

    return maps_left_cam, maps_right_cam, ROI1, ROI2