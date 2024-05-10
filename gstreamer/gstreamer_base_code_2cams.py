import cv2
from time import sleep, time
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
index = 0
delay = 5
while True:
        ret1, frame1 = cam1.read()
        ret2, frame2 = cam2.read()
        cv2.imshow('FRAMOS1',frame1)
        cv2.imshow('FRAMOS2', frame2)
        cv2.moveWindow('FRAMOS1', 0, 250)
        cv2.moveWindow('FRAMOS2', 1100, 250)

        keyEvent = cv2.waitKey(1)

        if keyEvent == ord('i'):
                sleep(0.5)
                cv2.imwrite('img_data/left_image_'+str(index)+'.jpg', frame1)
                cv2.imwrite('img_data/right_image_'+str(index)+'.jpg', frame2)
                index += 1

        #take a delayed picture, 
        if keyEvent == ord('d'):
                start = time()
                while time()- start <= delay:
                        ret1, frame1 = cam1.read()
                        ret2, frame2 = cam2.read()
                        cv2.imshow('FRAMOS1',frame1)
                        cv2.imshow('FRAMOS2', frame2)
                        cv2.moveWindow('FRAMOS1', 0, 250)
                        cv2.moveWindow('FRAMOS2', 1100, 250)

                cv2.imwrite('img_data/left_image_'+str(index)+'.jpg', frame1)
                cv2.imwrite('img_data/right_image_'+str(index)+'.jpg', frame2)
                index += 1

        if keyEvent==ord('q'):
                break

#close video capture object and close opencv window   
cam1.release()
cam2.release()
cv2.destroyAllWindows()