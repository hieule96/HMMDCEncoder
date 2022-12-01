# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 23:54:54 2021

@author: LE Trung Hieu
"""

import numpy as np
import sys,os
sys.path.insert(0, 'Lib/')
import Transform as tf
from itertools import repeat
import pyimgsaliency as psal

from matplotlib import pyplot as plt
from skimage.metrics import mean_squared_error,peak_signal_noise_ratio
import Quadtreelib as qd
import Optimizer as Opt
import re
import time
import pdb
class FrameYUV(object):
    def __init__(self, Y, U, V):
        self._Y = Y
        self._U = U
        self._V = V

def writenpArrayToFile(YUVArray,outputFileName,mode='wb'):
    with open(outputFileName,mode) as output:
        output.write(YUVArray[0].tobytes())
        output.write(YUVArray[2].tobytes())
        output.write(YUVArray[1].tobytes())

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

def read_YUV400_frame(fid, width, height,frame=0):
    # read a frame from a YUV420-formatted sequence
    fid.seek(frame*(width*height+width*height//2))
    Y_buf = fid.read(width * height)
    if (len(Y_buf)==width * height):
        Y = np.reshape(np.frombuffer(Y_buf, dtype=np.uint8), [height, width])
    else:
        Y=np.zeros((height,width))
    return FrameYUV(Y, 0, 0)    

CTU_path = "qtreeV.txt"
yuv_files = "resi.yuv"
Q1FileName = "QP1.csv"
Q2FileName = "QP2.csv"


bord_h = 288
bord_w = 352
step_w = np.ceil (bord_w/64)
step_h = np.ceil (bord_h/64)
nbCUinCTU = step_w*step_h
nbframeToEncode = 1
def mseToPSNR(mse):
    if mse !=0:
        return 10*np.log10(255**2/mse)
    else: 
        return 0
def buildModel(frame,frametype):
    with open(CTU_path,'r') as file:
        for lines in file:
            ParseTxt = lines
            matchObj  = re.sub('[<>]',"",ParseTxt)      
            matchObj  = re.sub('[ ]',",",matchObj)      
            chunk = matchObj.split(',')
            frame = int(chunk[0])
            pos = int(chunk[1])
            #print (lines)
            if (frame==frame):
                if pos == 0:
                    imgY= read_YUV420_frame(open(yuv_files,"rb"),bord_w,bord_h,0)._Y
                    saliance_map = psal.get_saliency_rbd(imgY)
                    lcu = qd.LargestCodingUnit(imgY.astype(int) - 128,1,8,64,64,frame)
                    step_w = int (np.around(lcu.w / lcu.block_size_w))
                quadtree_composition = chunk[2:]
                CTU = qd.Node(int (pos%step_w)*64,int (pos/step_w)*64,64,64,pos)
                if (frametype==0):
                    qd.import_subdivide(CTU,quadtree_composition,0,pos)
                lcu.CTUs.append(CTU)
                lcu.nbCTU += 1
                if pos == nbCUinCTU-1:
                    lcu.convert_Tree_childrenArray()
                    lcu.remove_bord_elements(lcu.w,lcu.h)
                    lcu.Init_aki()
                    lcu.merge_CTU()
                    lcu.updateWeight(saliance_map)
                    Oj = Opt.Optimizer_curvefitting(None,"exp3")
                    Oj.compteCurveCoefficientMultithread(lcu)
                    print (frame)
    return Oj,lcu
def worker_optimize(element,rN,Rt):
    element[0].changeParameter(Opt.OptimizerParameterLambdaCst(lam1=20.5,lam2=20.5,mu1=0.0,mu2=0.0,n0=0.5,QPmax=51,LCU=element[1],Dm=20,rN=rN,Rt = Rt))
    lcuOptimized = element[0].optimize_LCU()
    return lcuOptimized
if __name__=='__main__':
    if (len(sys.argv) > 4):
        Rt = float(sys.argv[1])
        rN = float(sys.argv[2])
        frame = int(sys.argv[3])
        frameType = int(sys.argv[4])
        print ("Process Frame %d Rt %.3f rN %.3f frametype%d"%(frame,Rt,rN,frameType))
    else:
        print("Optimization Failed missing arg %d" %len(sys.argv))
        sys.exit()
    tf.initROM()
    frameType = 0
    process_time_begin = time.time()
    optimizerInstanceTuple = buildModel(frame,frameType)
    listQP1_1 = []
    listQP2_2 = []
    lcu_o = worker_optimize(optimizerInstanceTuple,rN,Rt)
    listQP1_1+=lcu_o.Qi1
    listQP2_2+=lcu_o.Qi2
    if (frameType==0):
        with open(CTU_path,'r') as file:
            for lines in file:
                ParseTxt = lines
                matchObj  = re.sub('[<>]',"",ParseTxt) 
                matchObj  = re.sub('[ ]',",",matchObj)
                chunk = matchObj.split(',')
                posCTU = int(chunk[1])
                frame = int (chunk[0])
                pos_QP = 0
                if (frame==frame):
                    for element in chunk[2:]:
                        if (element=="99" or element=="8"):
                            try:
                                if (pos_QP < len(listQP1_1[posCTU])):
                                    listQP1_1[posCTU].insert(pos_QP,listQP1_1[posCTU][pos_QP])
                                    listQP2_2[posCTU].insert(pos_QP,listQP2_2[posCTU][pos_QP])
                                else:
                                    listQP1_1[posCTU].append(listQP1_1[posCTU][pos_QP-1])
                                    listQP2_2[posCTU].append(listQP2_2[posCTU][pos_QP-1])
                            except IndexError:
                                pdb.set_trace()
                        pos_QP+=1
                    posCTU +=1
    else:
        with open(CTU_path,'r') as file:
            for lines in file:
                ParseTxt = lines
                matchObj  = re.sub('[<>]',"",ParseTxt) 
                matchObj  = re.sub('[ ]',",",matchObj)
                chunk = matchObj.split(',')
                posCTU = int(chunk[1])
                frame = int (chunk[0])
                pos_QP = 0
                if (frame==frame):
                    for element in chunk[2:]:
                        listQP1_1[posCTU]+=[listQP1_1[posCTU][0]]
                        listQP2_2[posCTU]+=[listQP2_2[posCTU][0]]
                    posCTU +=1
    print ("Optimization Terminated: D1 (%.3f) D2(%.3f) R1(%d) R2(%d)" %(mseToPSNR(lcu_o.D1est), mseToPSNR(lcu_o.D2est), lcu_o.R1est *bord_h * bord_w,  lcu_o.R2est *bord_h * bord_w))
    # open the file in the write mode
    with open('QP1.csv', 'w') as f:
        for i in listQP1_1:
            for j in i:
                f.write("%d," %(j))
            f.write("\n")
    # open the file in the write mode
    with open('QP2.csv', 'w') as f:
        for i in listQP2_2:
            for j in i:
                f.write("%d," %(j))
            f.write("\n")