#Jetson Nano Series Lesson 14: Drawing Shapes on Video in OpenCV

import cv2
print(cv2.__version__)
dispW = 640
dispH = 480
flip=2
#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(0)
#cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

x = 0
y = 0
offset_x = 1
offset_y = 1

while True: 
    ret, frame = cam.read()
    #frame = cv2.rectangle(frame, (x,y), (80+x,50+y), (255, 0, 0), -1)
    frame = cv2.circle(frame, (20+x, 20+y), 20, (0,0,255), -1)

    x = x+offset_x
    y = y+offset_y

    if y+40 >= 480 or y <= 0:
        offset_y = -1 * offset_y

    if x+40 >= 640 or x <= 0:
        offset_x = -1 * offset_x


    cv2.imshow('WebCam', frame)
    cv2.moveWindow('WebCam', 0,0)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()