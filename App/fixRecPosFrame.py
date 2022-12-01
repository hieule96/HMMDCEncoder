#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 18:53:58 2022

@author: ubuntu
"""
import config
import YUVLib
from skimage.metrics import mean_squared_error as mse


outputFilePath = config.outputFilePath
mdcConfigPath = config.mdcConfigPath
sequencePath = config.sequencePath
resultPath = config.resultPath
libPath = config.libPath
QPPath = config.QPPath

inputSrcFileName = config.inputSrcFileName
pictureParam = config.pictureParam
listMDCFileName=[]
p = config.p
iteration = config.iteration
nbFrame = config.nbFrame
QPstep = config.QPstep
QP_min = config.QP_min

QPMstep = config.QPMstep
QPM_min = config.QPM_min
QPM_max = config.QPM_max


def fixingPosFrame():
    offset = 0
    for i in range (0,nbFrame):
        imgO = YUVLib.read_YUV420_frame(open(sequencePath+inputSrcFileName[0],"rb"),pictureParam.bord_w,pictureParam.bord_h,i)._Y
        img1 = YUVLib.read_YUV420_frame(open(resultPath+"rec_D1_noise_p_%.3f/rec_D1_noise_27_40_0.yuv"%(p),"rb"),pictureParam.bord_w,pictureParam.bord_h,i+offset)._Y
        if (mse(imgO,img1)>1000):
            mismatchlist = []
            for j in range (i,nbFrame):
                imgR = YUVLib.read_YUV420_frame(open(sequencePath+inputSrcFileName[0],"rb"),pictureParam.bord_w,pictureParam.bord_h,j)._Y
                mismatchlist.append(mse(img1,imgR))
            posmin = min(range(len(mismatchlist)), key=mismatchlist.__getitem__)
            print (posmin)
            offset = offset + posmin
fixingPosFrame()