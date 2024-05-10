import cv2
import numpy as np

def stereo_rectification_calibrated(leftFrame, rightFrame):
    #read the intrinsic parametres
    fs = cv2.FileStorage("calibration_params.yml", cv2.FILE_STORAGE_READ)
    calibParams = {'cameraMatrixLeft' : fs.getNode("cameraMatrixLeft").mat(), 
                   'distCoeffsLeft' : fs.getNode("distCoeffsLeft").mat(), 
                    'cameraMatrixRight' : fs.getNode("cameraMatrixRight").mat(), 
                    'distCoeffsRight' : fs.getNode("distCoeffsRight").mat(), 
                    'R' : fs.getNode("R").mat(), 
                    'T' : fs.getNode("T").mat() }
    
    #compute the extrinsic parameters from the intrinsic parameteres recieved from the calibration process
    #TODO: how to ge new ImageSize parameter ? 
    R1, R2, P1, P2, Q, ROI1, ROI2 = cv2.stereoRectify(calibParams['cameraMatrixLeft'], calibParams['distCoeffsLeft'], 
                                                    calibParams['cameraMatrixRight'], calibParams['distCoeffsRight'], 
                                                    (1920, 1080), calibParams['R'], calibParams['T'], alpha=-1, newImageSize=(270, 480) )
    
    #TODO: implement code to get undistortion and rectification transformation map
    maps_left_cam = []
    maps_right_cam = []
    maps_left_cam = cv2.initUndistortRectifyMap(calibParams['cameraMatrixLeft'], calibParams['distCoeffsLeft'], R1, P1, (1920, 1080), cv2.CV_16SC2)
    maps_right_cam = cv2.initUndistortRectifyMap(calibParams['cameraMatrixRight'], calibParams['distCoeffsRight'], R2, P2, (1920, 1080), cv2.CV_16SC2)

    print(ROI1)
    print(ROI2)

    #TODO: apply remapping to new image
    leftFrameRect = cv2.remap(leftFrame, maps_left_cam[0], maps_left_cam[1], cv2.INTER_LINEAR)
    rightFrameRect = cv2.remap(rightFrame, maps_right_cam[0], maps_right_cam[1], cv2.INTER_LINEAR)


    cv2.imshow('LEFT',leftFrameRect)
    cv2.imshow('RIGHT', rightFrameRect)
    cv2.moveWindow('LEFT', 100, 250)
    cv2.moveWindow('RIGHT', 1800, 250)

    while True:
       if cv2.waitKey(1) == ord('q'):
         break

    cv2.destroyAllWindows()