#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 12:08:57 2022

@author: ubuntu
"""
import sys,os
sys.path.insert(0, '../Lib')
import HEVCInterfaceDecoder
import MDCDecoderLib
from multiprocessing import Pool
import config
outputFilePath = config.outputFilePath
mdcConfigPath = config.mdcConfigPath
sequencePath = config.sequencePath
resultPath = config.resultPath
libPath = config.libPath
QPPath = config.QPPath
inputSrcFileName = config.inputSrcFileName
nbFrame = config.nbFrame
pictureParam = config.pictureParam
QPstep = config.QPstep
QP_min = config.QPmin

QPMstep = config.QPMstep
QPM_min = config.QPM_min
QPM_max = config.QPM_max
def workerMDC(obj):
    return obj.merge2Frame8x8(0,nbFrame)
def workerSDC(obj):
    return obj.computePSNRSequence(0,nbFrame)
def workerHEVC(obj):
    obj.decodeHEVC()
listMDCFileName = []
for i in range (QPM_min,QPM_max,QPMstep):
    for j in range (QP_min,i,QPstep):
        listMDCFileName.append([resultPath+"rec_D0/rec_D0_%d_%d.yuv"%(j,i),
                                resultPath+"rec_D1/rec_D1_%d_%d.yuv"%(j,i),
                                resultPath+"rec_D2/rec_D2_%d_%d.yuv"%(j,i)])

listSDCFileName = []
for i in range (QP_min,QPM_max,QPstep):
    listSDCFileName.append(resultPath+"rec_org/rec_org_%d.yuv"%(i))


if not os.path.exists(resultPath+'rec_D0'):
    os.makedirs(resultPath+'rec_D0')

listDecoderHevcD1 = []
listDecoderHevcD2 = []
for i in range (QPM_min,QPM_max,QPMstep):
    for j in range (QP_min,i,QPstep):
            listDecoderHevcD1.append(HEVCInterfaceDecoder.HEVCInterfaceDecoder(resultPath+"str_D1/str_D1_%d_%d.hevc" %(j,i),
                                                                            resultPath+"rec_D1/rec_D1_%d_%d.yuv"%(j,i),
                                                                            resultPath+"rec_D1/POC_D1_%d_%d.txt"%(j,i)))
            
            listDecoderHevcD2.append (HEVCInterfaceDecoder.HEVCInterfaceDecoder(resultPath+"str_D2/str_D2_%d_%d.hevc" %(j,i),
                                                                            resultPath+"rec_D2/rec_D2_%d_%d.yuv"%(j,i),
                                                                            resultPath+"rec_D2/POC_D2_%d_%d.txt"%(j,i)))
listDecoderMdcConfig = [MDCDecoderLib.DecoderConfigFile(yuvOrgFileName=sequencePath+inputSrcFileName[0],reconD0FileName=resultPath+i[0],
                                                          reconD1FileName=resultPath+i[1],reconD2FileName=resultPath+i[2]) 
                                                          for i in listMDCFileName]
listDecoderMdc = [MDCDecoderLib.DecoderMDC(i,pictureParam) for i in listDecoderMdcConfig]

listDecoderSdc = [MDCDecoderLib.DecoderSDC(sequencePath+i,sequencePath+inputSrcFileName[0],pictureParam) for i in listSDCFileName]

# with Pool() as p:
#     p.map(workerHEVC,listDecoderHevcD1)
# with Pool() as p:
#     p.map(workerHEVC,listDecoderHevcD2)
# with Pool() as p:
#     resultSDC = p.map(workerSDC,listDecoderSdc)
# with Pool() as p:
#     resultMDC = p.map(workerMDC,listDecoderMdc)




sizeD1 = []
sizeD2 = []
listQP = []
for i in range (QPM_min,QPM_max,QPMstep):
    for j in range (QP_min,i,QPstep):
        sizeD1.append(os.path.getsize(resultPath+"str_D1/str_D1_%d_%d.hevc"%(j,i))*8)
        sizeD2.append(os.path.getsize(resultPath+"str_D2/str_D2_%d_%d.hevc"%(j,i))*8)
        listQP.append([j,i])
if not os.path.exists(resultPath+'csv/'):
    os.makedirs(resultPath+'csv')
if not os.path.exists(resultPath+'csv/WithOutNoise'):
    os.makedirs(resultPath+'csv/WithOutNoise')

PerformanceSDC = []
for i,j in zip(range (QP_min,QPM_max,QPstep),resultSDC):
    PerformanceSDC.append([i,j[0],os.path.getsize(resultPath+"str_org/str_org_%d.hevc"%(i))*8])
PerformanceMDC = []
for i,j,k,l in zip(listQP,resultMDC,sizeD1,sizeD2):
    PerformanceMDC.append([i[0],i[1],j[0],int (k)+int(l),j[1],int(k),j[2],int(l)])


import pandas as pd
dfMDC = pd.DataFrame(PerformanceMDC,
                     columns=["QP","QPM","PSNR0","R0(bits)","PSNR1","R1(bits)","PSNR2","R2(bits)"]
                     )
dfMDC.to_csv(resultPath+"csv/WithOutNoise/Stat_MDC_CTUperSlice_300FH.csv",",",index=False)
dfSDC = pd.DataFrame(PerformanceSDC,
                     columns=["QP","PSNR","R(bits)"])
dfSDC.to_csv(resultPath+"csv/WithOutNoise/Stat_Encoder_CTUperSlice_300FH.csv",",",index=False)


#convert to kbps 25 FPS
dfSDC['R(Mbps)'] = (dfSDC['R(bits)']/1_000_000)*(25/nbFrame)
dfMDC['R0(Mbps)'] = (dfMDC['R0(bits)']/1_000_000)*(25/nbFrame)

import matplotlib.pyplot as plt
plt.plot(dfSDC['R(Mbps)'],dfSDC['PSNR'],label="SDC/R")
plt.plot(dfSDC['R(Mbps)']*2,dfSDC['PSNR'],label="SDC/2R")
for d in dfMDC.groupby(dfMDC['QPM']):
    plt.scatter(d[1]['R0(Mbps)'],d[1]['PSNR0'],marker='+',label="QPM%d"%(d[0]))
plt.xlabel("Rate(Mbps)")
plt.ylabel("E[PSNR] [dB]")
plt.legend(labelspacing=0.2,prop={'size':8})
plt.show()