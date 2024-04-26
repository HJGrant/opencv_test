#Jetson Nano Series Lesson 17: Drawing Shapes on Video in OpenCV

import cv2
import numpy as np
print(cv2.__version__)

evt=-1
coord = []
img=np.zeros((250,250,3), np.uint8)
def click(event, x, y, flags, params):
    global pnt 
    global evt

    if event == cv2.EVENT_LBUTTONDOWN:
        pnt = (x,y)
        coord.append(pnt)
        evt = event
        
    if event == cv2.EVENT_RBUTTONDOWN:
        print(x,y)
        blue = frame[y,x,0]
        green = frame[y,x,1]
        red = frame[y,x,2]
        print(blue, green, red)
        colorString = str(blue)+','+str(green)+','+str(red)
        img[:]=[blue, green, red]
        fnt = cv2.FONT_HERSHEY_PLAIN
        r=255-int(red)
        g=255-int(green)
        b=255-int(blue)
        tp=(b,g,r)
        cv2.putText(img, colorString, (10,25), fnt, 1, tp, 2)
        cv2.imshow('myColor', img)

dispW = 960
dispH = 720
flip=2
cv2.namedWindow('WebCam')
cv2.setMouseCallback('WebCam', click)
#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(0)
#cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

while True: 
    ret, frame = cam.read()

    for pnts in coord:
        cv2.circle(frame,pnts,5,(0,0,255), -1)
        cv2.putText(frame, str(pnts), pnts, cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,255,0), 2)

    cv2.imshow('WebCam', frame)
    cv2.moveWindow('WebCam', 0,0)

    keyEvent=cv2.waitKey(1)

    if keyEvent == ord('q'):
        break

    if keyEvent == ord('c'):
        coord=[]

cam.release()
cv2.destroyAllWindows()