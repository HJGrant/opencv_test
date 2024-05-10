import numpy as np 
import cv2 as cv
import glob2 as glob
import os

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((15*10,3), np.float32)
objp[:,:2] = np.mgrid[0:10,0:15].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

#include path to checkerboard image data, with which to calibrate the camera
images = glob.glob(os.path.join(os.getcwd(), 'img_data', 'left_image_*.jpg'))


for fname in images:
    img = cv.imread(fname)
    print(img)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (10,15), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
 
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

    # Draw and display the corners
    cv.drawChessboardCorners(img, (10,15), corners2, ret)
    cv.imshow('img', img)

    while True:
        if cv.waitKey(1) == ord('n'):
            break

    cv.destroyAllWindows()

#get distortion coefficients, camera matrix, rotation and translation vectors etc.
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

#get image and refine the camera matrix, either add extra black pixels to image or remove disorted pixels from the final image file
img = cv.imread(os.path.join(os.getcwd(), 'image_data', 'left12.jpg'))
h, w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

#undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
 
#crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('calibresult.png', dst)

#save multiple arrays with np.savez()
np.savez('B', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
data = np.load("camera_parameters.npz")

#read data by accesing via keyword argument
mtx1 = data['mtx']
dst1 = data['dist']

data.close()