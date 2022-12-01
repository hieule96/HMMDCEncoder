#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 11:26:10 2022

@author: ubuntu
"""

import numpy as np
import sys,os
sys.path.insert(0, '../Lib/')
import MDCDecoderLib
import Transform as tf

from matplotlib import pyplot as plt
from skimage.metrics import mean_squared_error,peak_signal_noise_ratio
import scipy
import Quadtreelib as qd
import Optimizer as Opt
import re
import time
import subprocess
import pickle

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

CTU_path = "qtreeAI.txt"
yuv_files = "../sequence/foreman_cif.yuv"
Q1FileName = "QP1.csv"
Q2FileName = "QP2.csv"
Q0FileName = "QP0.csv"
bord_h = 288
bord_w = 352
step_w = np.ceil (bord_w/64)
step_h = np.ceil (bord_h/64)
nbCUinCTU = 30
nbframeToEncode = 1
step_spliting = 10

def importLCU(frame_begin,frame_end):
    with open(CTU_path,'r') as file:
        for lines in file:
            ParseTxt = lines
            matchObj  = re.sub('[<>]',"",ParseTxt)      
            matchObj  = re.sub('[ ]',",",matchObj)      
            chunk = matchObj.split(',')
            frame = int(chunk[0])
            pos = int(chunk[1])
            #print (lines)
            if (frame>=frame_begin and frame<frame_end):
                if pos == 0:
                    imgY= read_YUV400_frame(open(yuv_files,"rb"),bord_w,bord_h,frame)._Y
                    lcu = qd.LargestCodingUnit(imgY.astype(int) - 128,1,8,64,64,frame)
                    step_w = int (np.around(lcu.w / lcu.block_size_w))
                quadtree_composition = chunk[2:]
                CTU = qd.Node(int (pos%step_w)*64,int (pos/step_w)*64,64,64)
                qd.import_subdivide(CTU,quadtree_composition,0)
                lcu.CTUs.append(CTU)
                lcu.nbCTU += 1
                if pos == nbCUinCTU-1:
                    lcu.convert_Tree_childrenArray()
                    lcu.remove_bord_elements(lcu.w,lcu.h)
                    lcu.Init_aki()
                    lcu.merge_CTU()
                    print (frame)
            if frame == frame_end:
                break
    return lcu

if __name__=='__main__':
    tf.initROM()
    precision_test = []
    list_optimizer_instance=[]
    process_time_begin = time.time()

    for i in range(0,1,1):
        list_optimizer_instance+=[importLCU(i,i+1)] 
    RTreal = 1.0
    rN = 0.03
    ## Compensation to have the exact real bit rate 
    # print ("rN:",rN)
    # with open('preprocessingFileOptimization.pkl','wb') as f:
    #     pickle.dump(list_optimizer_instance,f)

    # # Rt = scipy.optimize.bisect(optimize,0.90,1.70,args=(rN,RTreal),rtol=0.001,xtol = 0.001)
    # # print ("RT:%.3f"%Rt)
    Rt = 1.0
    rN = 0.0
    parameter = []
    Q1_List = []
    Q2_List = []
    listQP1_1 = []
    listQP2_2 = []
    for i in list_optimizer_instance:
        Oj = Opt.OptimizerReal(Opt.OptimizerParameterLambdaCst(lam1=20.5,lam2=20.5,mu1=0.1,mu2=0.1,n0=0.5,QPmax=51,LCU=i,Dm=20000,rN=rN,Rt = RTreal))
        x = Oj.optimizeQuadtreeLamCst()
    #     listQ1 = Q1.tolist()
    #     listQ2 = Q2.tolist()
    #     pos = 0
    #     for x in j.nbCUperCTU:
    #         listQP1_1.append(listQ1[pos:pos+x])
    #         listQP2_2.append(listQ2[pos:pos+x])
    #         pos+=x
    #     posCTU = 0
    # with open(CTU_path,'r') as file:
    #     for lines in file:
    #         ParseTxt = lines
    #         matchObj  = re.sub('[<>]',"",ParseTxt) 
    #         matchObj  = re.sub('[ ]',",",matchObj)
    #         chunk = matchObj.split(',')
    #         pos = int(chunk[1])
    #         pos_QP = 0
    #         for element in chunk[2:]:
    #             if (element=="99" or element=="8"):
    #                 if (pos_QP < len(listQP1_1[posCTU])):
    #                     listQP1_1[posCTU].insert(pos_QP,listQP1_1[posCTU][pos_QP])
    #                     listQP2_2[posCTU].insert(pos_QP,listQP2_2[posCTU][pos_QP])
    #                 else:
    #                     listQP1_1[posCTU].append(listQP1_1[posCTU][pos_QP-1])
    #                     listQP2_2[posCTU].append(listQP2_2[posCTU][pos_QP-1])
                       
    #             pos_QP+=1
    #         posCTU +=1

    # # open the file in the write mode
    # with open('QP1.csv', 'w') as f:
    #     for i in listQP1_1:
    #         for j in i:
    #             f.write("%d," %(j))
    #         f.write("\n")
    # # open the file in the write mode
    # with open('QP2.csv', 'w') as f:
    #     for i in listQP2_2:
    #         for j in i:
    #             f.write("%d," %(j))
    #         f.write("\n")  
    # # subprocess.call(['sh',"./testCompression.sh"], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    # r1 = os.path.getsize("QP1.hevc")
    # r2 = os.path.getsize("QP2.hevc")
    # #decode
    # pictureParam = MDCDecoderLib.PictureParamter(bord_w, bord_h, 1)
    # decoderCfg = MDCDecoderLib.DecoderMDCConfigFile(yuv_files,
    #                                 "rec_D0.yuv",
    #                                 "QP1.yuv",
    #                                 "QP2.yuv",
    #                                 0,
    #                                 0,
    #                                 "",
    #                                 "",
    #                                 "")
    # y = MDCDecoderLib.DecoderMDC(decoderCfg,pictureParam)
    # result_exact = y.merge2Frame8x8withlostFrameOracle_ffmpeg(80)
    # real_bpp1,real_bpp2 = r1*8/(bord_h*bord_w),r2*8/(bord_h*bord_w)
    # PSNR_est1,PSNR_est2 = 10*np.log10(255**2/D1_est),10*np.log10(255**2/D2_est)
    # print (Rt,rN,result_exact[0],result_exact[1],result_exact[2],PSNR_est1,PSNR_est2,real_bpp1,real_bpp2,R1_est,R2_est)
    # precision_test.append([Rt,rN,result_exact[0],result_exact[1],result_exact[2],PSNR_est1,PSNR_est2,real_bpp1,real_bpp2,R1_est,R2_est])
    # print ("Processing Time:", time.time() - process_time_begin)