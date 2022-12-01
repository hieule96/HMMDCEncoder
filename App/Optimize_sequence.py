# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 23:54:54 2021

@author: LE Trung Hieu
"""

import numpy as np
import sys,os
sys.path.insert(0, 'Lib/')
import MDCDecoderLib
import Transform as tf
from itertools import repeat
import pyimgsaliency as psal

from matplotlib import pyplot as plt
from skimage.metrics import mean_squared_error,peak_signal_noise_ratio
import scipy
import Quadtreelib as qd
import Optimizer as Opt
import re
import time
import subprocess
import pickle
from multiprocessing import Pool

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
yuv_files = "foreman_cif.yuv"
Q1FileName = "QP1.csv"
Q2FileName = "QP2.csv"
Q0FileName = "QP0.csv"

PSNR0_seq=[]
PSNR1_seq=[]
PSNR2_seq=[]
R0_seq = []
R0_AC_seq = []

bord_h = 288
bord_w = 352
step_w = np.ceil (bord_w/64)
step_h = np.ceil (bord_h/64)
nbCUinCTU = 30
nbframeToEncode = 1
step_spliting = 10

def buildModel(frame_begin,frame_end):
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
                    imgY= read_YUV420_frame(open(yuv_files,"rb"),bord_w,bord_h,frame)._Y
                    saliance_map = psal.get_saliency_rbd(imgY)
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
                    lcu.updateWeight(saliance_map)
                    Oj = Opt.Optimizer_curvefitting(None,"exp3")
                    Oj.computeCurveCoefficient(lcu)
                    print (frame)
            if frame == frame_end:
                break
    return Oj,lcu
def worker_buildModel(i):
    return buildModel(i,i+1)
def worker_optimize(element,rN,Rt):
    element[0].changeParameter(Opt.OptimizerParameterLambdaCst(lam1=20.5,lam2=20.5,mu1=0.0,mu2=0.0,n0=0.5,QPmax=51,LCU=element[1],Dm=20,rN=rN,Rt = Rt))
    lcuOptimized = element[0].optimize_LCU()
    return lcuOptimized
if __name__=='__main__':
    tf.initROM()
    precision_test = []
    list_optimizer_instance = []
    process_time_begin = time.time()
    listFrame = np.arange(0,1,1)
    with Pool() as p:
        list_optimizer_instance = p.map(worker_buildModel,listFrame)
    
    Rt = 1.0
    ResultSimulation = []
    rN = 0.1
    listQP1_1 = []
    listQP2_2 = []
    frame_begin = 0
    frame_end = 1
    with Pool() as p:
        lcu_o = p.starmap(worker_optimize,zip(list_optimizer_instance,repeat(rN),repeat(Rt)))
    for x in lcu_o:
        listQP1_1+=x.Qi1
        listQP2_2+=x.Qi2
    with open(CTU_path,'r') as file:
        for lines in file:
            ParseTxt = lines
            matchObj  = re.sub('[<>]',"",ParseTxt) 
            matchObj  = re.sub('[ ]',",",matchObj)
            chunk = matchObj.split(',')
            posCTU = int(chunk[1])
            frame = int (chunk[0])
            pos_QP = 0
            if (frame>=frame_begin and frame<frame_end):
                for element in chunk[2:]:
                    if (element=="99"):
                        if (pos_QP < len(listQP1_1[posCTU])):
                            listQP1_1[posCTU].insert(pos_QP,listQP1_1[posCTU][pos_QP])
                            listQP2_2[posCTU].insert(pos_QP,listQP2_2[posCTU][pos_QP])
                        else:
                            listQP1_1[posCTU].append(listQP1_1[posCTU][pos_QP-1])
                            listQP2_2[posCTU].append(listQP2_2[posCTU][pos_QP-1])
                    pos_QP+=1
                posCTU +=1

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
    # result = []
    # subprocess.call(['sh',"./testCompression.sh"], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    # r1 = os.path.getsize("QP1.hevc")
    # r2 = os.path.getsize("QP2.hevc")
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
    # result_noNoise = y.merge2Frame8x8withlostFrameOracle_ffmpeg(80)#,"ErrorDecodingFile1.txt","ErrorDecodingFile2.txt")

    # for i in range (0,10):
    #     #decode
    #     subprocess.call(['sh',"./simulate.sh"], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    #     pictureParam = MDCDecoderLib.PictureParamter(bord_w, bord_h, 1)
    #     decoderCfg = MDCDecoderLib.DecoderMDCConfigFile(yuv_files,
    #                                     "rec_D0.yuv",
    #                                     "QP1_n.yuv",
    #                                     "QP2_n.yuv",
    #                                     0,
    #                                     0,
    #                                     "",
    #                                     "",
    #                                     "")
    #     y = MDCDecoderLib.DecoderMDC(decoderCfg,pictureParam)
    #     y.resampleD1("QP1_resample.yuv","ErrorDecodingFile1.txt",80)
    #     y.resampleD2("QP2_resample.yuv","ErrorDecodingFile2.txt",80)
    #     pictureParam = MDCDecoderLib.PictureParamter(bord_w, bord_h, 1)
    #     decoderCfg = MDCDecoderLib.DecoderMDCConfigFile(yuv_files,
    #                                     "rec_D0.yuv",
    #                                     "QP1_resample.yuv",
    #                                     "QP2_resample.yuv",
    #                                     0,
    #                                     0,
    #                                     "",
    #                                     "",
    #                                     "")
    #     y = MDCDecoderLib.DecoderMDC(decoderCfg,pictureParam)
    #     result_exact = y.merge2Frame8x8withlostFrameOracle_ffmpeg(80)#,"ErrorDecodingFile1.txt","ErrorDecodingFile2.txt")
    #     result.append(result_exact)
    #     real_bpp1,real_bpp2 = r1*8/(bord_h*bord_w),r2*8/(bord_h*bord_w)
    # mean10Realisation = np.mean([result[i][0] for i in range(0,4)])
    # sigma10Realisation = np.mean([np.std(result[i][3]) for i in range (0,4)])
    # print (mean10Realisation,sigma10Realisation)
    # ResultSimulation.append([result_noNoise,mean10Realisation,sigma10Realisation,r1+r2])
    # PSNR_est1,PSNR_est2 = 10*np.log10(255**2/D1_est),10*np.log10(255**2/D2_est)
    # print (Rt,rN,result_exact[0],result_exact[1],result_exact[2],PSNR_est1,PSNR_est2,real_bpp1,real_bpp2,R1_est,R2_est)
    # precision_test.append([Rt,rN,result_exact[0],result_exact[1],result_exact[2],PSNR_est1,PSNR_est2,real_bpp1,real_bpp2,R1_est,R2_est])
    # print ("Processing Time:", time.time() - process_time_begin)

    
    # print (subprocess.Popen("./TAppEncoder -c MDC_cfg/encoder_intra_main-D1.cfg -c news_cif.cfg",shell=True, stdout=subprocess.PIPE).stdout.read())
    # print (subprocess.Popen("./TAppEncoder -c MDC_cfg/encoder_intra_main-D2.cfg -c news_cif.cfg",shell=True, stdout=subprocess.PIPE).stdout.read())
