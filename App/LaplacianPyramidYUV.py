#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 15:10:34 2022

@author: ubuntu
"""

import sys
import cv2 as cv
import pdb 
sys.path.insert(0, '../Lib/')
import YUVLib


with open("../sequence/ParkScene_1920x1080_24.yuv","rb") as fileI:
    with open("../sequence/ParkScene_1920x1080_24_0.yuv","wb") as fileO:
        with open("../sequence/ParkScene_1920x1080_24_R.yuv","wb") as fileR:
            for frame in range (0,240):
                img = YUVLib.read_YUV420_frame(fileI, 1920, 1080,frame)
                YUVArray = [[],[],[]]
                res =  [[],[],[]]
                YUVArray[0] = cv.pyrDown(img._Y)
                YUVArray[1] = cv.pyrDown(img._U)
                YUVArray[2] = cv.pyrDown(img._V)
                res[0] = img._Y.astype('int') - cv.pyrUp(YUVArray[0]) + 128
                res[1] = img._U.astype('int') - cv.pyrUp(YUVArray[1]) + 128
                res[2] = img._V.astype('int') - cv.pyrUp(YUVArray[2]) + 128
                # res[0] = cv.diff(img._Y, cv.pyrUp(YUVArray[0]))
                # res[1] = cv.diff(img._U, cv.pyrUp(YUVArray[1]))
                # res[2] = cv.diff(img._V, cv.pyrUp(YUVArray[2]))
                # pdb.set_trace()
                fileO.write(YUVArray[0].tobytes())
                fileO.write(YUVArray[1].tobytes())
                fileO.write(YUVArray[2].tobytes())
                fileR.write(res[0].astype('uint8').tobytes())
                fileR.write(res[1].astype('uint8').tobytes())
                fileR.write(res[2].astype('uint8').tobytes())

with open("../../SHM/bin/L0.yuv","rb") as L0File:
    with open("../../SHM/bin/L0Up.yuv","wb") as L0UpFile:
        for frame in range (0,23):
            imgL0 = YUVLib.read_YUV420_frame(L0File, 960, 540,frame)
            Y = cv.pyrUp(imgL0._Y)
            U = cv.pyrUp(imgL0._U)
            V = cv.pyrUp(imgL0._V)
            L0UpFile.write(Y.astype('uint8').tobytes())
            L0UpFile.write(U.astype('uint8').tobytes())
            L0UpFile.write(V.astype('uint8').tobytes())

with open("../../SHM/bin/L0.yuv","rb") as L0File:
    with open("../../SHM/bin/L1.yuv","rb") as L1File:
        with open ("../../SHM/bin/L1L2.yuv","wb") as L1L2File:
            for frame in range (0,23):
                imgL0 = YUVLib.read_YUV420_frame(L0File, 960, 540,frame)
                imgL1 = YUVLib.read_YUV420_frame(L1File,1920,1080,frame)
                rec =  [[],[],[]]
                res[0] =  cv.pyrUp(imgL0._Y) + imgL1._Y.astype('int') - 128
                res[1] =  cv.pyrUp(imgL0._U) + imgL1._U.astype('int') - 128
                res[2] =  cv.pyrUp(imgL0._V) + imgL1._V.astype('int') - 128
                L1L2File.write(res[0].astype('uint8').tobytes())
                L1L2File.write(res[1].astype('uint8').tobytes())
                L1L2File.write(res[2].astype('uint8').tobytes())

