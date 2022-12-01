# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:02:38 2021

@author: LE Trung Hieu
Obvious recontruction
"""
import cv2
import numpy as np
import sys,os
sys.path.insert(0, '../Lib/')

import Quadtreelib as qd
import re
import skimage.metrics
import pdb
import subprocess
import YUVLib

bord_h = 512
bord_w = 512
step_w = np.ceil (bord_w/64)
step_h = np.ceil (bord_h/64)
nbCUinCTU = 64
nbFrameToDecode = 1


class MDC_DEC_STATE:
    SEEK_FRAME = 0
    FRAME_PROCESSING = 1
    FRAME_WRITE = 2
def writenpArrayToFile(YUVArray,outputFileName,mode='wb'):
    with open(outputFileName,mode) as output:
        output.write(YUVArray[0].tobytes())
        output.write(YUVArray[2].tobytes())
        output.write(YUVArray[1].tobytes())

class PictureParamter():
    def __init__(self,w,h,nbCUinCTU,frameToEncode):
        self.bord_h = h
        self.bord_w = w
        self.nbCUinCTU=nbCUinCTU
        self.frameToEncode = frameToEncode
        self.step_w = np.ceil(w/64)
        self.step_h = np.ceil(h/64)
class DecoderConfigFile():
    def __init__(self,qTreeFileName,yuvOrgFileName,reconD1FileName,reconD2FileName,q1FileName,q2FileName):
        self.qTreeFileName = qTreeFileName
        self.reconD1FileName = reconD1FileName
        self.reconD2FileName = reconD2FileName
        self.yuvOrgFileName = yuvOrgFileName
        self.q1FileName = q1FileName
        self.q2FileName = q2FileName
def assignBlock(x,y,blockSize,YUVJoint,Frame):
    x_half = x//2
    y_half = y//2
    blockSize_half = blockSize//2
    YUVJoint[0][y:y+blockSize,x:x+blockSize] = Frame._Y[y:y+blockSize,x:x+blockSize]
    YUVJoint[2][y_half:y_half+blockSize_half,x_half:x_half+blockSize_half] = Frame._U[y_half:y_half+blockSize_half,x_half:x_half+blockSize_half] 
    YUVJoint[1][y_half:y_half+blockSize_half,x_half:x_half+blockSize_half] = Frame._V[y_half:y_half+blockSize_half,x_half:x_half+blockSize_half]
def checkDecision(x,y,blockSize,imgO,img1,img2):
    decision_MSE = 0
    mseblock1 = skimage.metrics.mean_squared_error(imgO._Y[y:y+blockSize,x:x+blockSize],img1._Y[y:y+blockSize,x:x+blockSize])
    mseblock2 = skimage.metrics.mean_squared_error(imgO._Y[y:y+blockSize,x:x+blockSize],img2._Y[y:y+blockSize,x:x+blockSize])
    if mseblock1>mseblock2:
        decision_MSE = 2
    elif mseblock1<mseblock2:
        decision_MSE = 1
    return decision_MSE

def decodeFrame(configFile,pictureParam):
    dec_state = MDC_DEC_STATE.SEEK_FRAME
    frame = 0
    PNSR_mean = 0
    P1 = 0
    P2 = 0
    P0 = 0
    with open(configFile.qTreeFileName,'r') as qtFile:
        with open(configFile.q1FileName,'r') as quant1File:
            with open(configFile.q2FileName,'r') as quant2File:
                while (True):
                    if (dec_state == MDC_DEC_STATE.SEEK_FRAME):
                        img1 = YUVLib.read_YUV420_frame(open(configFile.reconD1FileName,"rb"),pictureParam.bord_w,pictureParam.bord_h,frame)
                        img2 = YUVLib.read_YUV420_frame(open(configFile.reconD2FileName,"rb"),pictureParam.bord_w,pictureParam.bord_h,frame)
                        imgO = YUVLib.read_YUV420_frame(open(configFile.yuvOrgFileName,"rb"),pictureParam.bord_w,pictureParam.bord_h,frame)
                        YUVJoint = [[],[],[]]
                        YUVJoint[0] = np.zeros((img1._Y.shape[0],img1._Y.shape[1]),dtype=np.uint8)
                        YUVJoint[1] = np.zeros((img1._V.shape[0],img1._V.shape[1]),dtype=np.uint8)
                        YUVJoint[2] = np.zeros((img1._U.shape[0],img1._U.shape[1]),dtype=np.uint8)
                        dec_state = MDC_DEC_STATE.FRAME_PROCESSING
                        print ("SEEK YUV ",(frame))
                    elif (dec_state == MDC_DEC_STATE.FRAME_PROCESSING):
                        for lines in qtFile:
                            ParseTxt = lines
                            matchObj  = re.sub('[<>]',"",ParseTxt)      
                            matchObj  = re.sub('[ ]',",",matchObj)      
                            chunk = matchObj.split(',')
                            position_cu = int(chunk[1])
                            quadtree_composition = chunk[2:]
                            CTU = qd.Node(int (position_cu%pictureParam.step_w)*64,int (position_cu/pictureParam.step_w)*64,64,64)
                            qd.import_subdivide(CTU,quadtree_composition,0)
                            Q1 = quant1File.readline().split(",")
                            Q2 = quant2File.readline().split(",")
                            cus = qd.find_children(CTU)
                            #Remove bord elements
                            remove_list = []
                            i = 0
                            for cu in cus:
                                if(cu.x0 > pictureParam.bord_w or cu.y0>pictureParam.bord_h or cu.x0+cu.width > pictureParam.bord_w or cu.y0+cu.height > pictureParam.bord_h):
                                    remove_list.append(i)
                                i = i + 1
                            i = 0
                            for pos in remove_list:
                                # print (ctu_index,remove_list)
                                cus.pop(pos-i)
                                i = i + 1
                            for index in range (0,len(cus)):
                                decision = 0
                                testdecision = checkDecision(cus[index].x0,cus[index].y0,cus[index].height,imgO,img1,img2)
                                if (testdecision!=decision and testdecision!=0):
                                    decision=testdecision
                                if decision == 1:
                                    assignBlock(cus[index].x0,cus[index].y0,cus[index].height,YUVJoint,img1)
                                elif decision == 2:
                                    assignBlock(cus[index].x0,cus[index].y0,cus[index].height,YUVJoint,img2)
                                elif decision == 0:
                                    assignBlock(cus[index].x0,cus[index].y0,cus[index].height,YUVJoint,img2)
                            if (position_cu >= pictureParam.nbCUinCTU-1):
                                dec_state = MDC_DEC_STATE.FRAME_WRITE
                                break
                    elif (dec_state == MDC_DEC_STATE.FRAME_WRITE):
                        P1 = skimage.metrics.peak_signal_noise_ratio(imgO._Y,img1._Y)
                        P2 = skimage.metrics.peak_signal_noise_ratio(imgO._Y,img2._Y)
                        P0 = skimage.metrics.peak_signal_noise_ratio(imgO._Y,YUVJoint[0],data_range=255)
                        print ("WRITE_FRAME %s PNSR1: %s PSNR2: %s PSNR0: %s" %(frame,P1,P2,P0))
                        PNSR_mean = P0 + PNSR_mean 
                        YUVJoint[0] = YUVJoint[0].ravel()
                        YUVJoint[1] = YUVJoint[1].ravel()
                        YUVJoint[2] = YUVJoint[2].ravel()
                        if (frame == 0):
                            writenpArrayToFile(YUVJoint,"rec_D0.yuv",'wb')
                        else:
                            writenpArrayToFile(YUVJoint,"rec_D0.yuv",'ab')
                        dec_state = MDC_DEC_STATE.SEEK_FRAME
                        frame = frame + 1
                    if (frame >= pictureParam.frameToEncode):
                        print ("BREAK")
                        PSNR_mean = PNSR_mean/pictureParam.frameToEncode
                        print ("PNSR0 mean",PSNR_mean)
                        break
    return P0,P1,P2

DecQtreeFile = "qtreeV.txt"
if __name__ == "__main__":
    decoderConfigFile = DecoderConfigFile(qTreeFileName=DecQtreeFile, yuvOrgFileName ="../sequence/lena400.yuv",reconD1FileName="QP1.yuv", reconD2FileName="QP2.yuv", q1FileName="QP1.csv", q2FileName="QP2.csv")
    pictureParam=PictureParamter(bord_w,bord_h,nbCUinCTU,1)
    decodeFrame(decoderConfigFile,pictureParam)
    imgO = YUVLib.read_YUV420_frame(open("foreman_cif.yuv","rb"),pictureParam.bord_w,pictureParam.bord_h,0)
    imgNoiseMDC = YUVLib.read_YUV420_frame(open("rec_D0.yuv","rb"),pictureParam.bord_w,pictureParam.bord_h,0)
    imgNoiseSDC = YUVLib.read_YUV420_frame(open("rec_org.yuv","rb"),pictureParam.bord_w,pictureParam.bord_h,0)
    print ("MDC " + str(skimage.metrics.peak_signal_noise_ratio(imgO._Y,imgNoiseMDC._Y)))
    print ("SDC " + str(skimage.metrics.peak_signal_noise_ratio(imgO._Y,imgNoiseSDC._Y)))