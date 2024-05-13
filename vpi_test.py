import vpi
import numpy as np
import cv2
import matplotlib.pyplot as plt

def depth_map_vpi():
    left_dummy = np.ndarray((512,256, 3), np.uint8)
    right_dummy = np.ndarray((512,256, 3), np.uint8)

    left_dummy_gray = cv2.cvtColor(left_dummy, cv2.COLOR_RGB2GRAY)
    right_dummy_gray = cv2.cvtColor(right_dummy, cv2.COLOR_RGB2GRAY)

    left_frame = vpi.asimage(left_dummy_gray, vpi.Format.U8)
    right_frame = vpi.asimage(right_dummy_gray, vpi.Format.U8)

    with vpi.Backend.CUDA:
        output = vpi.stereodisp(left_frame, right_frame, window=5, maxdisp=64) \
                    .convert(vpi.Format.U8, scale=1.0/(32*64)*255)

    with output.rlock_cuda() as data:
        print(data)

def depth_map_vpi_gray():
    left_frame = vpi.Image((512,256), vpi.Format.U8)
    right_frame = vpi.Image((512,256), vpi.Format.U8)

    with vpi.Backend.CUDA:
        output = vpi.stereodisp(left_frame, right_frame, window=5, maxdisp=64) \
                    .convert(vpi.Format.U8, scale=1.0/(32*64)*255)

    with output.rlock_cuda() as data:
        print(data)


#example of vpi input image, conversion, and reading with lock statement
def vpi_use_algorithm():
    #input = vpi.Image((512,256), vpi.Format.RGB8)
    data = np.ndarray((512,256,3), np.uint8)
    input = vpi.asimage(data)

    with vpi.Backend.CUDA:
        output = input.convert(vpi.Format.U8)

    with output.rlock_cuda() as data:
        img = vpi.asimage(data)

    #with vpi.Backend.CPU:
    #    img_conv = img.convert(vpi.Format.U8)

    with img.rlock_cpu() as data:
        print(data)
    

#vpi_use_algorithm()
vpi_use_algorithm()