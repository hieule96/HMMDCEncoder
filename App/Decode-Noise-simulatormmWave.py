#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 15:33:30 2022

@author: ubuntu
"""
import sys,os
sys.path.insert(0, '../Lib/')
import MDCDecoderLib
from multiprocessing import Pool
import config

outputFilePath = config.outputFilePath
mdcConfigPath = config.mdcConfigPath
sequencePath = config.sequencePath
resultPath = config.resultPath
libPath = config.libPath
QPPath = config.QPPath
pictureParam = config.pictureParam

mmWaveOutputPath="../hinted/"
 
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


decparam = MDCDecoderLib.DecoderMDCConfigFile(yuvOrgFileName=sequencePath+inputSrcFileName[0],
                                                        reconD0FileName=mmWaveOutputPath+"MDC0.yuv",
                                                        reconD1FileName=mmWaveOutputPath+"MDC1.yuv",
                                                        reconD2FileName=mmWaveOutputPath+"MDC2.yuv")
decoderinstance = MDCDecoderLib.DecoderMDC(decparam,pictureParam)
decoderinstance.resampleD1(mmWaveOutputPath+"MDC_1_padding.yuv",mmWaveOutputPath+"qtree1.txt",nbFrame)
decoderinstance.resampleD2(mmWaveOutputPath+"MDC_2_padding.yuv",mmWaveOutputPath+"qtree2.txt",nbFrame)
# x = decoderinstance.merge2Frame8x8withlostFrameOracle(99,mmWaveOutputPath+"qtree1.txt",mmWaveOutputPath+"qtree2.txt")
y = decoderinstance.merge2Frame8x8withlostFrameOracle_ffmpeg(nbFrame-1)
