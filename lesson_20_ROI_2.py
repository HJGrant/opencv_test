import cv2
print(cv2.__version__)
dispW=640
dispH=480
flip=2

evt = -1
coord = []

def click(event, x=0, y=0, flags, params):
    global pnt 
    global evt

    if event == cv2.EVENT_LBUTTONDOWN:
        pnt = (x,y)
        coord.append(pnt)
        evt = event


cv2.namedWindow('WebCam')
cv2.setMouseCallback('WebCam', click)
cam=cv2.VideoCapture(0)

x = 0
y = 0
offset_x = 1
offset_y = 1

while True:
    ret, frame = cam.read()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameGray = cv2.cvtColor(frameGray, cv2.COLOR_GRAY2BGR)
    frameGray = cv2.rectangle(frameGray, (x,y), (80+x,50+y), (255, 0, 0), 2)
    roi = frame[y:y+50, x:x+80].copy()
    frameGray[y:y+50, x:x+80] = roi


    cv2.imshow('WebCam',frameGray)
    cv2.moveWindow('WebCam', 0, 0)

    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()