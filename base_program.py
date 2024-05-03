import cv2
import _dbus_glib_bindings
print(cv2.__version__)
dispW=640
dispH=480
flip=2
#Uncomment These next Two Line for Pi Camera
#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=RG12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#cam= cv2.VideoCapture(camSet)

#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
cam = cv2.VideoCapture(1)

if not cam.isOpened():
 print("Cannot open camera")
 exit()

while True:
    ret, frame = cam.read()

    cv2.rectangle(frame, (10, 10), (210, 210))

    cv2.imshow('FRAMOS',frame)
    cv2.moveWindow('FRAMOS', 0, 0)

    if cv2.waitKey(1)==ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()