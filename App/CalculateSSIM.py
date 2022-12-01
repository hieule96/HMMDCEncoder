#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 14:24:21 2022

@author: ubuntu
"""
import sys
import config
from multiprocessing import Pool
from skimage.metrics import structural_similarity as ssim


sys.path.insert(0, '../Lib')
import YUVLib

outputFilePath = config.outputFilePath
mdcConfigPath = config.mdcConfigPath
sequencePath = config.sequencePath
resultPath = config.resultPath
libPath = config.libPath
QPPath = config.QPPath

inputSrcFileName = config.inputSrcFileName
pictureParam = config.pictureParam
listMDCFileName=[]
listSDCFileName=[]
p = config.p
iteration = config.iteration
nbFrame = config.nbFrame
QPstep = config.QPstep
QP_min = config.QP_min

QPMstep = config.QPMstep
QPM_min = config.QPM_min
QPM_max = config.QPM_max


def calculateMeanSSIM(recFile,orgFile,nbFrame):
    ssim_mean = 0
    for frame in range (0,nbFrame):
        img1 = YUVLib.read_YUV420_frame(open(recFile,"rb"),pictureParam.bord_w,pictureParam.bord_h,frame)
        imgO = YUVLib.read_YUV420_frame(open(orgFile,"rb"),pictureParam.bord_w,pictureParam.bord_h,frame)
        ssim_mean = ssim_mean + ssim(imgO._Y,img1._Y,datarange=255)
    ssim_mean = ssim_mean / (frame+1)
    return ssim_mean

for i in range (QPM_min,QPM_max,QPMstep):
    for j in range (QP_min,i,QPstep):
        for it in range (iteration):
            listMDCFileName.append([resultPath+"rec_D0_noise_p_%.3f/rec_D0_noise_%d_%d_%d.yuv"%(p,j,i,it)])

for i in range (QP_min,QPM_max,QPstep):
    for it in range (iteration):
        listSDCFileName.append(resultPath+"rec_org_noise_p_%.3f/rec_org_noise_%d_%d.yuv.yuv"%(p,i,it))

listMDC = [(i[0],sequencePath+inputSrcFileName[0],nbFrame) for i in listMDCFileName]
listSDC = [(i[0],sequencePath+inputSrcFileName[0],nbFrame) for i in listSDCFileName]

with Pool () as p:
    SSIM_MDC = p.starmap(calculateMeanSSIM,listMDC)
with Pool () as p:
    SSIM_SDC = p.starmap(calculateMeanSSIM,listSDC)