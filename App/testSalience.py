#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 13:45:03 2022

@author: ubuntu
"""

from skimage.restoration import denoise_nl_means,estimate_sigma
from skimage import img_as_float,img_as_ubyte
import numpy as np
import matplotlib.pyplot as  plt
import pyimgsaliency as psal

yuv_files = "../sequence/foreman_cif.yuv"
bord_h = 288
bord_w = 352
frame = 0
class FrameYUV(object):
    def __init__(self, Y, U, V):
        self._Y = Y
        self._U = U
        self._V = V

def read_YUV420_frame(fid, width, height,frame=0):
    # read a frame from a YUV420-formatted sequence
    d00 = height // 2
    d01 = width // 2
    fid.seek(frame*(width*height+width*height//2))
    Y_buf = fid.read(width * height)
    Y = np.reshape(np.frombuffer(Y_buf, dtype=np.uint8), [height, width])
    U_buf = fid.read(d01 * d00)
    U = np.reshape(np.frombuffer(U_buf, dtype=np.uint8), [d00, d01])
    V_buf = fid.read(d01 * d00)
    V = np.reshape(np.frombuffer(V_buf, dtype=np.uint8), [d00, d01])
    return FrameYUV(Y, U, V)

imgY_ubytes= read_YUV420_frame(open(yuv_files,"rb"),bord_w,bord_h,frame)._Y
rbd = psal.get_saliency_rbd(imgY_ubytes)
plt.imshow(rbd,cmap="gray")
plt.show()