import cv2
print(cv2.__version__)

def __gstreamer_pipeline(
        camera_id,
        sensor_mode=2,          #4 = 3856x2180 and 90fps; 3 = 3856 x 2180 FR = 29.999999 fps; 2 = 1928 x 1090 FR = 59.999999 fps;
        capture_width=3856,
        capture_height=2180,
        display_width=1920,
        display_height=1080,
        framerate=30,
        flip_method=0,
    ):
    return (
            "nvarguscamerasrc sensor-id=%d sensor-mode=%d buffer-list=True blocksize=12609120 ! "       #12609120
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d,"
            "format=(string)NV12 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! "
            "appsink "
            % (
                    camera_id,
                    sensor_mode,
                    capture_width,
                    capture_height,
                    flip_method,
                    display_width,
                    display_height
            )
    )

#funciton for defining the gstreamer pipelin string
#def __gstreamer_pipeline(
#       camera_id,
#        capture_width=1920,
#        capture_height=1080,
#        display_width=1920/2,
#        display_height=1080/2,
#        framerate=60,
#        flip_method=0,
#    ):
#    return (
#            "nvarguscamerasrc sensor-id=%d ! "
#            "video/x-raw(memory:NVMM), "
#            "width=(int)%d, height=(int)%d, "
#            "format=(string)NV12, framerate=(fraction)%d/1 ! "
#            "nvvidconv flip-method=%d ! "
#            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
#           "videoconvert ! "
#            "video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=True"
#            % (
#                    camera_id,
#                    capture_width,
#                    capture_height,
#                    framerate,
#                    flip_method,
#                    display_width,
#                    display_height,
#            )
#    )