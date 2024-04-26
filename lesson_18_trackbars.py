#Jetson Nano Series´Lesson 18: trackbars 
#completed homework

import cv2
print(cv2.__version__)
dispW = 960
dispH = 720
flip=2

def nothing():
    pass

cam = cv2.VideoCapture(0)
cv2.namedWindow('WebCam')
cv2.createTrackbar('xVal_pos', 'WebCam', 0, 500, nothing)
cv2.createTrackbar('yVal_pos', 'WebCam', 0, 500, nothing)
cv2.createTrackbar('xVal_w', 'WebCam', 25, 500, nothing)
cv2.createTrackbar('yVal_h', 'WebCam', 25, 500, nothing)
#cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

while True: 
    ret, frame = cam.read()
    xVal_pos = cv2.getTrackbarPos('xVal_pos', 'WebCam')
    yVal_pos = cv2.getTrackbarPos('yVal_pos', 'WebCam')
    xVal_w = cv2.getTrackbarPos('xVal_w', 'WebCam')
    yVal_h = cv2.getTrackbarPos('yVal_h', 'WebCam')
    cv2.rectangle(frame, (xVal_pos, yVal_pos), (xVal_pos+xVal_w, yVal_pos+yVal_h), (255,0,0), 3)

    cv2.imshow('WebCam', frame)
    cv2.moveWindow('WebCam', 10,10)
 
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
