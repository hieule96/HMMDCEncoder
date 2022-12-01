#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 18:33:05 2022

@author: ubuntu
"""

import numpy as np
import YUVLib

class PictureParamter():
    def __init__(self,w,h,nbCUinCTU,frameToEncode):
        self.bord_h = h
        self.bord_w = w
        self.nbCUinCTU=nbCUinCTU
        self.frameToEncode = frameToEncode
class OptimizerInputFile():
    def __init__(self,inputYUVFile):
        self.inputYUVFile = inputYUVFile
def deltadr_right(lamj, muj, Ej, Cij):
    value = -lamj /((Cij / (1 + Cij)) + muj * Ej)
    return value
def computesigmablock(block):
    return np.std(block-np.mean(block))
def getSectionImage(x0,y0,blockSize,imgsrc):
    return imgsrc[y0:y0+blockSize,x0:x0+blockSize]
def optimize(imgsrc,pictureParam):
    #utilize formula delta D/ delta R = -0.85*2**(QP-12)/3
    #Ci generation
    Ci1 = []
    Ci2 = []
    for i in range(0,pictureParam.nbCUinCTU):
        if (i%2==0):
            Ci1.append(0.001)
            Ci2.append(1)
        else:
            Ci1.append(1)
            Ci2.append(0.001)
    Ci1 = np.array(Ci1)
    Ci2 = np.array(Ci2)
    #compute QP for each
    y1 = deltadr_right(1,0.1,0,Ci1)
    y2 = deltadr_right(1,0.1,0,Ci2)
    #Applied our formula
    QP1 = 3*np.log2(-y1/0.85)+12
    QP2 = 3*np.log2(-y2/0.85)+12
    return QP1,QP2
def writeQPTestCaseToFile(QP1,QP2):
    np.savetxt("QP1.csv",QP1,delimiter="\n",fmt='%d')
    np.savetxt("QP2.csv",QP2,delimiter="\n",fmt="%d")

        
picParam = PictureParamter(352,288,30,1)
imgsrc = YUVLib.read_YUV420_frame(open("news_cif.yuv","rb"), picParam.bord_w, picParam.bord_h)
QP1,QP2 = optimize(imgsrc._Y,picParam)
writeQPTestCaseToFile(QP1,QP2)
