import cv2


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