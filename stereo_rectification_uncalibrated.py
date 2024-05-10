import cv2
import numpy as np
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

def stereo_rectification_uncalibrated(leftFrame, rightFrame):
    sift = cv2.SIFT_create()

    #use SIFT algorithm to get keypoints in left and right frame
    kp1, des1 = sift.detectAndCompute(leftFrame, None)
    kp2, des2 = sift.detectAndCompute(rightFrame, None)

    #use FLANN algorithm to match keypoints in both frames
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, tree=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    #matchesMask = [[0,0] for i in range(len(matches))]
    good = []
    pts1 = []
    pts2 = []

    for i, (m,n) in enumerate(matches):
       if m.distance < 0.7*n.distance:
          good.append(m)
          pts2.append(kp2[m.trainIdx].pt)
          pts1.append(kp1[m.queryIdx].pt)


    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)
    fundamental_matrix, inliers = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)

    pts1 = pts1[inliers.ravel() == 1]
    pts2 = pts2[inliers.ravel() == 1]

    #use this function to show epilines correspondance in both frames
    #show_epilines(leftFrame, rightFrame, fundamental_matrix, pts1, pts2)
    
    h1, w1 = leftFrame.shape
    h2, w2 = rightFrame.shape

    #compute the homography matrices from the fundamental matrix and the keypoints
    _, H1, H2 = cv2.stereoRectifyUncalibrated(np.float32(pts1), np.float32(pts2), fundamental_matrix, imgSize=(w1, h1))

    #rectify the left and right frame with the homography matrices
    leftFrameRect = cv2.warpPerspective(leftFrame, H1, (w1, h1))
    rightFrameRect = cv2.warpPerspective(rightFrame, H2, (w2, h2))

    return H1, H2

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

#read first frame and get parameters
ret1, frame1 = cam1.read()
ret2, frame2 = cam2.read()
h1, w1 = frame1.shape
h2, w2 = frame2.shape

#compute homography matrices from first two frames
H1, H2 = stereo_rectification_uncalibrated(frame1, frame1)

#Main loop
while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()
    frame1, frame2 = stereo_rectification_uncalibrated(frame1, frame2)
    cv2.imshow('FRAMOS1',frame1)
    cv2.imshow('FRAMOS2', frame2)
    cv2.moveWindow('FRAMOS1', 0, 250)
    cv2.moveWindow('FRAMOS2', 1100, 250)

    if cv2.waitKey(1)==ord('q'):
        break

#close video capture object and close opencv window   
cam1.release()
cam2.release()
cv2.destroyAllWindows()