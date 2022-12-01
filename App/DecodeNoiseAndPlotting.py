#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 16:30:46 2022

@author: ubuntu

Decode Noise signal and MDC
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

if not os.path.exists(resultPath+'rec_D2_noise_p_%.3f/'%(p)):
    os.makedirs(resultPath+'rec_D2_noise_p_%.3f/'%(p))
if not os.path.exists(resultPath+'rec_D1_noise_p_%.3f/'%(p)):
    os.makedirs(resultPath+'rec_D1_noise_p_%.3f/'%(p))
if not os.path.exists(resultPath+'rec_D0_noise_p_%.3f/'%(p)):
    os.makedirs(resultPath+'rec_D0_noise_p_%.3f/'%(p))
if not os.path.exists(resultPath+'rec_org_noise_p_%.3f'%(p)):
    os.makedirs(resultPath+'rec_org_noise_p_%.3f'%(p))
    
def workerMDC(obj,POCFile1,POCFile2):
    print ("worker MDC %s \n" %(POCFile1))
    return obj.merge2Frame8x8withlostFrameSansOracle(nbFrame,POCFile1,POCFile2)
def workerSDC(obj,POCFile,recFile):
    return obj.computePSNRwithmissing(nbFrame,POCFile,recFile)
def workerHEVC(obj):
    print ("Worker HEVC")
    obj.decodeHEVC()
listDecoderHevcNoiseD1=[]
listDecoderHevcNoiseD2=[]
for i in range (QPM_min,QPM_max,QPMstep):
    for j in range (QP_min,i,QPstep):
        for it in range (iteration):
            listDecoderHevcNoiseD1.append(HEVCInterfaceDecoder.HEVCInterfaceDecoder(resultPath+"str_D1_noise_p_%.3f/str_D1_%d_%d_%d.hevc" %(p,j,i,it),
                                                                            resultPath+"rec_D1_noise_p_%.3f/rec_D1_noise_%d_%d_%d.yuv"%(p,j,i,it),
                                                                            resultPath+"rec_D1_noise_p_%.3f/POC_D1_noise_%d_%d_%d.txt"%(p,j,i,it)))
            
            listDecoderHevcNoiseD2.append (HEVCInterfaceDecoder.HEVCInterfaceDecoder(resultPath+"str_D2_noise_p_%.3f/str_D2_%d_%d_%d.hevc" %(p,j,i,it),
                                                                            resultPath+"rec_D2_noise_p_%.3f/rec_D2_noise_%d_%d_%d.yuv"%(p,j,i,it),
                                                                            resultPath+"rec_D2_noise_p_%.3f/POC_D2_noise_%d_%d_%d.txt"%(p,j,i,it)))
        
            listMDCFileName.append([resultPath+"rec_D0_noise_p_%.3f/rec_D0_noise_%d_%d_%d.yuv"%(p,j,i,it),
                                            resultPath+"rec_D1_noise_p_%.3f/rec_D1_noise_%d_%d_%d.yuv"%(p,j,i,it),
                                            resultPath+"rec_D2_noise_p_%.3f/rec_D2_noise_%d_%d_%d.yuv"%(p,j,i,it)])

        
listDecoderMdcConfig = [MDCDecoderLib.DecoderConfigFile(yuvOrgFileName=sequencePath+inputSrcFileName[0],
                                                        reconD0FileName=resultPath+i[0],
                                                        reconD1FileName=resultPath+i[1],
                                                        reconD2FileName=resultPath+i[2]) 
                                                      for i in listMDCFileName]
listSDCFileName = []
listDecoderHevcNoiseOrg=[]
for i in range (QP_min,QPM_max,QPstep):
    for it in range (iteration):
        listDecoderHevcNoiseOrg.append(HEVCInterfaceDecoder.HEVCInterfaceDecoder(resultPath+"str_org_noise_p_%.3f/str_org_%d_%d.hevc" %(p,i,it),
                                                                        resultPath+"rec_org_noise_p_%.3f/rec_org_noise_%d_%d.yuv"%(p,i,it),
                                                                        resultPath+"rec_org_noise_p_%.3f/POC_org_noise_%d_%d.txt"%(p,i,it)))
        listSDCFileName.append(resultPath+"rec_org_noise_p_%.3f/rec_org_noise_%d_%d.yuv"%(p,i,it))
listDecoderSdc = [MDCDecoderLib.DecoderSDC(resultPath+i,sequencePath+inputSrcFileName[0],pictureParam) for i in listSDCFileName]
listDecoderMdc = [MDCDecoderLib.DecoderMDC(i,pictureParam) 
                  for i in listDecoderMdcConfig]
listDecoderMDCWithParam = [(i,j.qtreeDecFile,k.qtreeDecFile) 
                           for i,j,k in zip(listDecoderMdc,listDecoderHevcNoiseD1,listDecoderHevcNoiseD2)]
listDecoderSDCWithParam = [(i,j.qtreeDecFile,i.sdcFileName+".yuv") 
                           for i,j in zip(listDecoderSdc,listDecoderHevcNoiseOrg)]

# with Pool() as pool:
#     pool.map(workerHEVC,listDecoderHevcNoiseD2)
# with Pool() as pool:
#     pool.map(workerHEVC,listDecoderHevcNoiseD1)
# with Pool() as pool:
#     pool.map(workerHEVC,listDecoderHevcNoiseOrg)
with Pool() as pool:
    resultMDCit = pool.starmap(workerMDC,listDecoderMDCWithParam)
with Pool() as pool:
    resultSDCit = pool.starmap(workerSDC,listDecoderSDCWithParam)

# x= workerMDC(*listDecoderMDCWithParam[0])
# print (x)
def mean_iteration_MDC(result_multipleit,iteration):
    resultMDC_it_mean = []
    PSNR_mean_it0 = 0
    PSNR_mean_it1 = 0
    PSNR_mean_it2 = 0
    SSIM_mean_it0 = 0
    SSIM_mean_it1 = 0
    SSIM_mean_it2 = 0
    
    #processing Iteration mean
    for i in range (len (result_multipleit)):
        PSNR_mean_it0 = PSNR_mean_it0 + result_multipleit[i][0]
        PSNR_mean_it1 = PSNR_mean_it1 + result_multipleit[i][1]
        PSNR_mean_it2 = PSNR_mean_it2 + result_multipleit[i][2]
        if (i%iteration == iteration-1):
            PSNR_mean_it0=PSNR_mean_it0/iteration
            PSNR_mean_it1=PSNR_mean_it1/iteration
            PSNR_mean_it2=PSNR_mean_it2/iteration
            resultMDC_it_mean.append([PSNR_mean_it0,PSNR_mean_it1,PSNR_mean_it2,SSIM_mean_it0,SSIM_mean_it1,SSIM_mean_it2])
            PSNR_mean_it0 = 0
            PSNR_mean_it1 = 0
            PSNR_mean_it2 = 0
    return resultMDC_it_mean
def mean_iteration_SDC(result_multipleit,iteration):
    resultMDC_it_mean = []
    PSNR_mean_it= 0
    #processing Iteration mean
    for i in range (len (result_multipleit)):
        PSNR_mean_it = PSNR_mean_it + result_multipleit[i][0]
        if (i%iteration == iteration-1):
            PSNR_mean_it=PSNR_mean_it/iteration
            resultMDC_it_mean.append([PSNR_mean_it])
            PSNR_mean_it= 0
    return resultMDC_it_mean
mean_precision = 0
for i in resultMDCit:
    mean_precision = mean_precision + i[4]
mean_precision = mean_precision / len(resultMDCit)
print ("Mean precision %f"%(mean_precision))

resultMDC = mean_iteration_MDC(resultMDCit,iteration)
resultSDC = mean_iteration_SDC(resultSDCit,iteration)

if not os.path.exists(resultPath+'csv/'):
    os.makedirs(resultPath+'csv')
if not os.path.exists(resultPath+'csv/WithNoise'):
    os.makedirs(resultPath+'csv/WithNoise')

import csv
with open(resultPath+'csv/WithNoise/'+"Raw_MDC_%s_%d_%.3f.csv"%(inputSrcFileName[0],nbFrame,p), "w") as f:
    writer = csv.writer(f)
    writer.writerows(resultMDCit)
with open(resultPath+'csv/WithNoise/'+"Raw_SDC_%s_%d_%.3f.csv"%(inputSrcFileName[0],nbFrame,p), "w") as f:
    writer = csv.writer(f)
    writer.writerows(resultSDCit)

sizeD1 = []
sizeD2 = []
listQP = []
for i in range (QPM_min,QPM_max,QPMstep):
    for j in range (QP_min,i,QPstep):
        sizeD1.append(os.path.getsize(resultPath+"str_D1/str_D1_%d_%d.hevc"%(j,i))*8)
        sizeD2.append(os.path.getsize(resultPath+"str_D2/str_D2_%d_%d.hevc"%(j,i))*8)
        listQP.append([j,i])

PerformanceMDC = []
for i,j,k,l in zip(listQP,resultMDC,sizeD1,sizeD2):
    PerformanceMDC.append([i[0],i[1],j[0],int (k)+int(l),j[1],int(k),j[2],int(l)])
PerformanceSDC = []
for i,j in zip(range (QP_min,QPM_max,QPstep),resultSDC):
    PerformanceSDC.append([i,j[0],os.path.getsize(resultPath+"str_org/str_org_%d.hevc"%(i))*8])
import pandas as pd
import matplotlib.pyplot as plt
dfMDC = pd.DataFrame(PerformanceMDC,
                      columns=["QP","QPM","PSNR0","R0(bits)","PSNR1","R1(bits)","PSNR2","R2(bits)"]
                      )
dfMDC.to_csv(resultPath+"csv/WithNoise/Stat_MDC_%s_noise_%dFH_%.3f.csv"%(inputSrcFileName[0],nbFrame,p),",",index=False)
dfSDC = pd.DataFrame(PerformanceSDC,
                      columns=["QP","PSNR","R(bits)"])
dfSDC.to_csv(resultPath+"csv/WithNoise/Stat_Encoder_%s_%dFH_%.3f.csv"%(inputSrcFileName[0],nbFrame,p),",",index=False)

#convert to kbps 25 FPS
dfSDC['R(Mbps)'] = (dfSDC['R(bits)']/1_000_000)*(25/nbFrame)
dfMDC['R0(Mbps)'] = (dfMDC['R0(bits)']/1_000_000)*(25/nbFrame)

plt.plot(dfSDC['R(Mbps)'],dfSDC['PSNR'],label="SDC/R",marker="+")
list_marker = ["v","2",'h',"D","s"]
for d,mark in zip(dfMDC.groupby(dfMDC['QPM']),list_marker):
        plt.plot(d[1]['R0(Mbps)'],d[1]['PSNR0'],label="QPM%d"%(d[0]),marker=mark)
plt.xlabel("Rate(Mbps)")
plt.ylabel("E[PSNR] [dB]")
plt.legend(labelspacing=0.2,prop={'size':8})
plt.show()


# plt.plot(dfSDC['R(Mbps)'],dfSDC['SSIM'],label="SDC/R",marker="+")
# list_marker = ["v","2",'h',"D","s"]
# for d,mark in zip(dfMDC.groupby(dfMDC['QPM']),list_marker):
#         plt.plot(d[1]['R0(Mbps)'],d[1]['SSIM0'],label="QPM%d"%(d[0]),marker=mark)
# plt.xlabel("Rate(Mbps)")
# plt.ylabel("E[PSNR] [dB]")
# plt.legend(labelspacing=0.2,prop={'size':8})
# plt.show()