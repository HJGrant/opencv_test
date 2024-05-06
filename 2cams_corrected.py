import cv2
import numpy as np
print(cv2.__version__)

#funciton for defining the gstreamer pipelin string
#Note: you may need to find a setting here to set the latency of gstreamer to 0
def __gstreamer_pipeline(
        camera_id,
        capture_width=1920,
        capture_height=1080,
        display_width=1920/2,
        display_height=1080/2,
        framerate=30,
        flip_method=0,
    ):
    return (
            "nvarguscamerasrc sensor-id=%d ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=True"
            % (
                    camera_id,
                    capture_width,
                    capture_height,
                    framerate,
                    flip_method,
                    display_width,
                    display_height,
            )
    )

def stereo_correct(frameLeft, frameRight):
    h, w = frameLeft.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(params[0], params[1], (w,h), 1, (w,h))
    dstLeft = cv2.undistort(frameLeft, params[0], params[1], None, newcameramtx)

    x, y, w, h = roi
    frameLeft = dstLeft[y:y+h, x:x+w]

    h, w = frameRight.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(params[2], params[3], (w,h), 1, (w,h))
    dstRight = cv2.undistort(frameRight, params[2], params[3], None, newcameramtx)
    #frameRight = cv2.undistort(frameRight, params[2], params[3], None, params[2])

    x, y, w, h = roi
    frameRight = dstRight[y:y+h, x:x+w]

    print(frameRight.shape)
    print(frameLeft.shape)


    return frameLeft, frameRight

rightData = np.load("camera_parameters_right.npz")
leftData = np.load("camera_parameters_left.npz")
#fs = cv2.FileStorage("calibration_params.yml", cv2.FILE_STORAGE_READ)
#params = [fs.getNode("cameraMatrixLeft").mat(), fs.getNode("distCoeffsLeft").mat(), fs.getNode("cameraMatrixRight").mat(), fs.getNode("distCoeffsRight").mat()]
params = [leftData['mtx'], leftData['dist'], rightData['mtx'], rightData['dist']]


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


#Main loop
while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()
    frame1, frame2 = stereo_correct(frame1, frame2)
    cv2.imshow('FRAMOS1',frame1)
    cv2.imshow('FRAMOS2', frame2)
    cv2.moveWindow('FRAMOS1', 0, 250)
    cv2.moveWindow('FRAMOS2', 1100, 250)

    if cv2.waitKey(1)==ord('q'):
        break

#close video capture object and close opencv window   
cam1.release()
cam2.release()
cv2.destroyAllWindows()