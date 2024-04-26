#code from Paul McWhorters youtube video series on AI with the Jetson Nano

import cv2
print(cv2.__version__)
dispW = 960
dispH = 720
flip=2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(0)
#cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

while True: 
    ret, frame = cam.read()
    cv2.imshow('WebCam', frame)
    cv2.moveWindow('WebCam', 700,0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frameSmall = cv2.resize(frame, (320, 240))
    graySmall = cv2.resize(gray, (320, 240)) 
    cv2.imshow('BW', graySmall)
    cv2.imshow('WebCam', frameSmall)
    cv2.moveWindow('BW', 0, 265)
    cv2.moveWindow('WebCam', 0, 0)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
