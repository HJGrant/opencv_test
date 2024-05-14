import cv2
from time import sleep, time
from gstreamer.gstreamer_base_code import __gstreamer_pipeline, __gstreamer_pipeline_no_extras
print(cv2.__version__)

#initialise video capture object   
cam1 = cv2.VideoCapture(__gstreamer_pipeline_no_extras(camera_id=0, flip_method=0), cv2.CAP_GSTREAMER)
cam2 = cv2.VideoCapture(__gstreamer_pipeline_no_extras(camera_id=1, flip_method=0), cv2.CAP_GSTREAMER)

#check if video capture object was properly initialised and able to open
if not cam1.isOpened():
 print("Cannot open camera 1")
 exit()

if not cam2.isOpened():
 print("Cannot open camera 2")
 exit()


#Main loop
index = 0
while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    print(frame1.shape)
    print(frame2.shape)

    cv2.imshow('FRAMOS1',frame1)
    cv2.imshow('FRAMOS2', frame2)
    cv2.moveWindow('FRAMOS1', 0, 250)
    cv2.moveWindow('FRAMOS2', 1100, 250)

    keyEvent = cv2.waitKey(1)

    if keyEvent == ord('i'):
        sleep(0.5)
        cv2.imwrite('img_data/left_image_'+str(index)+'.png', frame1)
        cv2.imwrite('img_data/right_image_'+str(index)+'.png', frame2)
        index += 1

    if keyEvent == ord('d'):
        start = time()
        while time()- start <= 5:
                ret1, frame1 = cam1.read()
                ret2, frame2 = cam2.read()
                cv2.imshow('FRAMOS1',frame1)
                cv2.imshow('FRAMOS2', frame2)
                cv2.moveWindow('FRAMOS1', 0, 250)
                cv2.moveWindow('FRAMOS2', 1100, 250)

        cv2.imwrite('img_data/left_image_'+str(index)+'.png', frame1)
        cv2.imwrite('img_data/right_image_'+str(index)+'.png', frame2)
        index += 1

    if keyEvent==ord('q'):
        break

#close video capture object and close opencv window   
cam1.release()
cam2.release()
cv2.destroyAllWindows()