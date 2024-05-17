import cv2
import vpi
import numpy as np

def vpi_stereo(left_frame, right_frame):
    #set the max disparities in the disparity map
    max_disp = 250
    min_disp = 0         #original 16
    num_disp = 200       #original 64
    block_size = 9             #original 8
    disp12MaxDiff = 50         #original 1
    uniquenessRatio = 0       #original 1
    quality = 8
    p1 = 0
    p2 = 0

    #convert images to graysale 
    #left_gray = cv2.cvtColor(left_frame, cv2.COLOR_BGR2GRAY)
    #right_gray = cv2.cvtColor(right_frame, cv2.COLOR_BGR2GRAY)

    left_frame = left_frame.astype('uint8')
    right_frame = right_frame.astype('uint8')

    #read in grayscale images as vpi image objects
    left_frame_vpi = vpi.asimage(left_frame, vpi.Format.U8)
    right_frame_vpi = vpi.asimage(right_frame, vpi.Format.U8)

    #perform processing with CUDA backend, especially stereo disparity calculation
    #TODO: setup bars to allow tuning of the stereo disparity computation params
    with vpi.Backend.CUDA:
        disparity = vpi.stereodisp(left_frame_vpi, right_frame_vpi, window=block_size, maxdisp=max_disp, mindisp=min_disp, 
                                   quality=quality, uniqueness=uniquenessRatio, p1=p1, p2=p2, 
                                   includediagonals=False).convert(vpi.Format.U8, scale=1.0/(32*max_disp)*255)

        #I don't know what this does, refer to stereo disp example in docs 
        if disparity.format == vpi.Format.S16_BL:
            disparity = disparity.convert(vpi.Format.S16, backend=vpi.Backend.VIC)

        #convert to unsigned8 and rescale for values to be between 0 and 255; also copy data from CUDA to cpu to recieve numpy array
        disparity = disparity.convert(vpi.Format.U8, scale=255.0/(32*max_disp)).cpu()

        #apply a color map to the disparity image
        #disparityColor = cv2.applyColorMap(disparity, cv2.COLORMAP_JET)

    #with disparity.rlock_cuda() as data:
    #    disp_img = vpi.asimage(data)

    #with disparity.rlock_cpu() as data:
    #    mtx = data

    #return the color disparity map
    return disparity