import cv2
print(cv2.__version__)
dispW=640
dispH=480
flip=2

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

    x = x+offset_x
    y = y+offset_y

    if y+40 >= 480 or y <= 0:
        offset_y = -1 * offset_y
    if x+40 >= 640 or x <= 0:
        offset_x = -1 * offset_x

    cv2.imshow('WebCam',frameGray)
    cv2.moveWindow('WebCam', 0, 0)

    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()