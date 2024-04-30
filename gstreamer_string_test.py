import cv2
print(cv2.__version__)

#funciton for defining the gstreamer pipelin string
def __gstreamer_pipeline(
        camera_id,
        capture_width=1920,
        capture_height=1080,
        display_width=1920,
        display_height=1080,
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
#cam = cv2.VideoCapture(__gstreamer_pipeline(camera_id=0, flip_method=0), cv2.CAP_GSTREAMER)
camSet="nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! nvvidconv flip-method=0 ! video/x-raw, width=1920, height=1080, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink"
cam= cv2.VideoCapture(camSet, cv2.CAP_GSTREAMER)

#check if video capture object was properly initialised and able to open
if not cam.isOpened():
 print("Cannot open camera")
 exit()


#Main loop
while True:
    ret, frame = cam.read()
    cv2.imshow('FRAMOS',frame)
    cv2.moveWindow('FRAMOS', 0, 0)

    if cv2.waitKey(1)==ord('q'):
        break

#close video capture object and close opencv window   
cam.release()
cv2.destroyAllWindows()