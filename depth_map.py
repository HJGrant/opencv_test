import cv2
import numpy as np
from matplotlib import pyplot as plt

#function for defining the gstreamer string
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

#initialise video capture object   
cam1 = cv2.VideoCapture(__gstreamer_pipeline(camera_id=0, flip_method=0), cv2.CAP_GSTREAMER)
cam2 = cv2.VideoCapture(__gstreamer_pipeline(camera_id=1, flip_method=0), cv2.CAP_GSTREAMER)

#read one frame from each camera and convert to grayscale
ret1, frame1 = cam1.read()
ret2, frame2 = cam2.read()
frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

#display both frames
while True:
        cv2.imshow('FRAMOS1',frame1)
        cv2.imshow('FRAMOS2', frame2)
        cv2.moveWindow('FRAMOS1', 0, 250)
        cv2.moveWindow('FRAMOS2', 1100, 250)

        if cv2.waitKey(1)==ord('q'):
                break

cam1.release()
cam2.release()
cv2.destroyAllWindows()

stereo = cv2.StereoBM.create(numDisparities=32, blockSize=15)
disparity = stereo.compute(frame1, frame2)
fig1 = plt.figure(figsize=(1,2))
fig1.add_subplot(1,2, 1)
plt.imshow(disparity, 'gray')
fig1.add_subplot(1,2, 2)
plt.imshow(frame1,'gray')
plt.show()