import cv2 as cv
#import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import numpy as np

def drawlines(img1,img2,lines,pts1,pts2):
        ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
        r,c = img1.shape
        img1 = cv.cvtColor(img1,cv.COLOR_GRAY2BGR)
        img2 = cv.cvtColor(img2,cv.COLOR_GRAY2BGR)

        for r,pt1,pt2 in zip(lines,pts1,pts2):
                color = tuple(np.random.randint(0,255,3).tolist())
                x0,y0 = map(int, [0, -r[2]/r[1] ])
                x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
                img1 = cv.line(img1, (x0,y0), (x1,y1), color,1)
                img1 = cv.circle(img1,tuple(pt1),5,color,-1)
                img2 = cv.circle(img2,tuple(pt2),5,color,-1)
        return img1,img2

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
cam1 = cv.VideoCapture(__gstreamer_pipeline(camera_id=1, flip_method=0), cv.CAP_GSTREAMER)
cam2 = cv.VideoCapture(__gstreamer_pipeline(camera_id=0, flip_method=0), cv.CAP_GSTREAMER)

#check if video capture object was properly initialised and able to open
if not cam1.isOpened():
 print("Cannot open camera 1")
 exit()

if not cam2.isOpened():
 print("Cannot open camera 2")
 exit()

#read one frame from each camera
ret1, frame1 = cam1.read()
ret2, frame2 = cam2.read()
frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)

#display both frames
while True:
        cv.imshow('FRAMOS1',frame1)
        cv.imshow('FRAMOS2', frame2)
        cv.moveWindow('FRAMOS1', 0, 250)
        cv.moveWindow('FRAMOS2', 1100, 250)

        if cv.waitKey(1)==ord('q'):
                break

cam1.release()
cam2.release()
cv.destroyAllWindows()


sift = cv.SIFT_create()
 
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(frame1,None)
kp2, des2 = sift.detectAndCompute(frame2,None)
 
# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)
 
flann = cv.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1,des2,k=2)
 
pts1 = []
pts2 = []
 
# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
        if m.distance < 0.8*n.distance:
                pts2.append(kp2[m.trainIdx].pt)
                pts1.append(kp1[m.queryIdx].pt)

#find the fundamental matrix, which relates one camera to another camera in pixel coordinates taking rotaion and translation into considration
pts1 = np.int32(pts1)
pts2 = np.int32(pts2)
F, mask = cv.findFundamentalMat(pts1,pts2,cv.FM_LMEDS)
 
# We select only inlier points
pts1 = pts1[mask.ravel()==1]
pts2 = pts2[mask.ravel()==1]


# Find epilines corresponding to points in right image (second image) and
# drawing its lines on left image
lines1 = cv.computeCorrespondEpilines(pts2.reshape(-1,1,2), 2,F)
lines1 = lines1.reshape(-1,3)
img5,img6 = drawlines(frame1,frame2,lines1,pts1,pts2)
 
# Find epilines corresponding to points in left image (first image) and
# drawing its lines on right image
lines2 = cv.computeCorrespondEpilines(pts1.reshape(-1,1,2), 1,F)
lines2 = lines2.reshape(-1,3)
img3,img4 = drawlines(frame2,frame1,lines2,pts2,pts1)
 
plt.subplot(121),plt.imshow(img5)
plt.subplot(122),plt.imshow(img3)
plt.show()
