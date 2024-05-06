import yaml
import cv2
import os
import numpy as np
import glob2 as glob

fs = cv2.FileStorage("calibration_params.yml", cv2.FILE_STORAGE_READ)
#fn = fs.getNode("cameraMatrixLeft")
#print(fn.mat())

mtxLeft = fs.getNode("cameraMatrixLeft").mat()
distLeft = fs.getNode("distCoeffsLeft").mat()

mtxRight = fs.getNode("cameraMatrixRight").mat()
distRight = fs.getNode("distCoeffsRight").mat()

imagesLeft = glob.glob(os.path.join(os.getcwd(), 'img_data', 'left_image_*.jpg'))
imagesRight = glob.glob(os.path.join(os.getcwd(), 'img_data', 'right_image_*.jpg'))

for fname in imagesLeft: 
    base=os.path.basename(fname)
    fn = os.path.splitext(base)[0]

    img = cv2.imread(fname)

    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtxLeft, distLeft, (w,h), 1, (w,h))

    dst = cv2.undistort(img, mtxLeft, distLeft, None, newcameramtx)

    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite('new_data/new_'+fn+'.png', dst)


for fname in imagesRight:
    base=os.path.basename(fname)
    fn = os.path.splitext(base)[0]

    img = cv2.imread(fname)

    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtxRight, distRight, (w,h), 1, (w,h))

    dst = cv2.undistort(img, mtxRight, distRight, None, newcameramtx)

    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite('new_data/new_'+fn+'.png', dst)