import cv2
import numpy as np
from gstreamer.gstreamer_base_code_2cams import __gstreamer_pipeline
print(cv2.__version__)

def drawlines(img1src, img2src, lines, pts1src, pts2src):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r, c = img1src.shape
    img1color = cv2.cvtColor(img1src, cv2.COLOR_GRAY2BGR)
    img2color = cv2.cvtColor(img2src, cv2.COLOR_GRAY2BGR)
    # Edit: use the same random seed so that two images are comparable!
    np.random.seed(0)
    for r, pt1, pt2 in zip(lines, pts1src, pts2src):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2]/r[1]])
        x1, y1 = map(int, [c, -(r[2]+r[0]*c)/r[1]])
        img1color = cv2.line(img1color, (x0, y0), (x1, y1), color, 1)
        img1color = cv2.circle(img1color, tuple(pt1), 5, color, -1)
        img2color = cv2.circle(img2color, tuple(pt2), 5, color, -1)
    return img1color, img2color

def show_epilines(img1, img2, fundamental_matrix, pts1, pts2):
    lines1 = cv2.computeCorrespondEpilines(
    pts2.reshape(-1, 1, 2), 2, fundamental_matrix)
    lines1 = lines1.reshape(-1, 3)
    img5, img6 = drawlines(img1, img2, lines1, pts1, pts2)

    # Find epilines corresponding to points in left image (first image) and
    # drawing its lines on right image
    lines2 = cv2.computeCorrespondEpilines(
    pts1.reshape(-1, 1, 2), 1, fundamental_matrix)
    lines2 = lines2.reshape(-1, 3)
    img3, img4 = drawlines(img2, img1, lines2, pts2, pts1)

    plt.subplot(121), plt.imshow(img5)
    plt.subplot(122), plt.imshow(img3)
    plt.suptitle("Epilines in both images")
    plt.show()

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

#read 2 images in order ot get dimensions and compute first homography matrix
img1 = cv2.imread("img_data/left_image_1.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("img_data/right_image_1.jpg", cv2.IMREAD_GRAYSCALE)

#Main loop
h1, w1 = img1.shape
h2, w2 = img2.shape
H1, H2 = stereo_rectification_uncalibrated(img1, img2)

while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    left_frame_rectified = cv2.warpPerspective(frame1, H1, (w1, h1))
    right_frame_rectified = cv2.warpPerspective(frame2, H2, (w2, h2))

    cv2.imshow('LEFT FRAME',left_frame_rectified)
    cv2.imshow('RIGH FRAME', right_frame_rectified)
    cv2.moveWindow('LEFT FRAME', 100, 250)
    cv2.moveWindow('RIGHT FRAME', 1100, 250)
     
    if cv2.waitKey(1)==ord('q'):
        break

#close video capture object and close opencv window   
cam1.release()
cam2.release()
cv2.destroyAllWindows()