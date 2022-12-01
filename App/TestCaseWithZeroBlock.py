#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 09:45:29 2021

@author: ubuntu
"""

import os,glob,sys
from multiprocessing import Pool

sys.path.insert(0, '../Lib')
import MDCDecoderLib
import HEVCInterfaceEncoder


YUV1 = [[],[],[]]
YUV2 = [[],[],[]]
outputFilePath = "../outputs/"
mdcConfigPath = "../MdcCfgns/"
sequencePath = "../sequence/"
resultPath ="../result/"
libPath = "../Lib/"
QPPath = "../QP/"
listSeqCfgFileName = ["foreman_cif_1F.cfg"]
inputSrcFileName = ["foreman_cif.yuv"]
listEncCfgD1FileName = ["encoder_intra_main-D1.cfg"]
listEncCfgD2FileName = ["encoder_intra_main-D2.cfg"]
listEncCfgorgFileName = ["encoder_intra_main.cfg"]

nbCTU = 30
wFrame = 352
hFrame = 288
pictureParam = MDCDecoderLib.PictureParamter(352, 288, 30, 1)

# def calculateEntropyofHEVC(wFrame,hFrame,filename="test.txt"):
#     list_element=[]
#     with open(filename) as transformedresidualfile:
#         for line in transformedresidualfile:
#             currentline = line.split(",")
#             list_element+=(currentline)
#     coeff = np.array(list_element,dtype=np.int)
#     values, counts= np.unique(coeff, return_counts = True)
#     probs = counts/len(coeff)
#     ent = 0.0
#     # Compute entropy
#     for i in probs:
#       ent -= i *log(i, 2)
#     #convert to bpp
#     #Total entropy is entropy bit per symbol to bit perframe
#     entropyTotal = ent * len(coeff)
#     #Entropy in bpp (bit per pixel)
#     entbpp = entropyTotal/(wFrame*hFrame)
#     return entbpp
# def silentremove(filename):
#     try:
#         os.remove(filename)
#     except OSError as e: # this would be "except OSError, e:" before Python 2.6
#         if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
#             raise # re-raise exception if a different error occurred
def worker(obj):
    obj.runHEVCEncoderNoVerbose2()
def workerMDC(obj):
    return obj.merge2Frame8x8(0,1)
def workerSDC(obj):
    return obj.computePSNRSequence(0,1)
def createObjList():
    listD1FileName = []
    listD2FileName = []
    QPMD1_done = [i[2] for i in listD1FileName]
    QPD1_done =[i[1] for i in listD1FileName]
    QPMD2_done =[i[2] for i in listD2FileName]
    QPD2_done =[i[1] for i in listD2FileName]
    if not os.path.exists(resultPath+'str_D1_1F'):
        os.makedirs(resultPath+'str_D1_1F')
    if not os.path.exists(resultPath+'str_D2_1F'):
        os.makedirs(resultPath+'str_D2_1F')
    if not os.path.exists(resultPath+'rec_D1_1F'):
        os.makedirs(resultPath+'rec_D1_1F')
    if not os.path.exists(resultPath+'rec_D2_1F'):
        os.makedirs(resultPath+'rec_D2_1F')   
    for i in range (5,51,5):
        for j in range (0,i,1):
            if (j not in QPD1_done and i not in QPMD1_done):
                listD1FileName.append([resultPath+"str_D1_1F/str_D1_%d_%d.hevc"%(j,i),resultPath+"rec_D1_1F/rec_D1_%d_%d.yuv"%(j,i),QPPath+"QP1_%d_%d.csv"%(j,i),(i+j)/2])
            if (j not in QPD2_done and i not in QPMD2_done):
                listD2FileName.append([resultPath+"str_D2_1F/str_D2_%d_%d.hevc"%(j,i),resultPath+"rec_D2_1F/rec_D2_%d_%d.yuv"%(j,i),QPPath+"QP2_%d_%d.csv"%(j,i),(i+j)/2])
    listEncoderHevcD1 = [HEVCInterfaceEncoder.HEVCEncoder(mdcConfigPath+listEncCfgD1FileName[0],
                                                          sequencePath+listSeqCfgFileName[0],
                                                          i[0],i[1],i[2],i[3]) for i in listD1FileName]
    listEncoderHevcD2 = [HEVCInterfaceEncoder.HEVCEncoder(mdcConfigPath+listEncCfgD2FileName[0],
                                                          sequencePath+listSeqCfgFileName[0],
                                                          i[0],i[1],i[2],i[3]) for i in listD2FileName]
    return listEncoderHevcD1,listEncoderHevcD2

def runPoolEncoder():
    listEncoderHevcD1,listEncoderHevcD2 = createObjList()
    list_worker = []
    for i,j in zip (listEncoderHevcD1,listEncoderHevcD2):
        list_worker.append(i)
        list_worker.append(j)
    with Pool() as p:
        p.map(worker,list_worker)
def runPoolRefEncoder():
    if not os.path.exists(resultPath+'str_org_1F'):
        os.makedirs(resultPath+'str_org_1F')
    if not os.path.exists(resultPath+'rec_org_1F'):
        os.makedirs(resultPath+'rec_org_1F')   
    listFileRef = []
    for i in range (0,51,1):
        listFileRef.append([resultPath+"str_org_1F/str_org_%d.hevc"%(i),resultPath+"rec_org_1F/rec_org_%d.yuv"%(i),"",i])
    listEncoderHevcOrg = [HEVCInterfaceEncoder.HEVCEncoder(mdcConfigPath+listEncCfgorgFileName[0],
                                                          sequencePath+listSeqCfgFileName[0],
                                                          i[0],i[1],i[2],i[3]) for i in listFileRef]
    with Pool() as p:
        p.map(worker,listEncoderHevcOrg)
def decodeMdc(pictureParam):
    listMDCFileName = []
    for i in range (5,51,5):
        for j in range (0,i,1):
            listMDCFileName.append([resultPath+"rec_D0_1F/rec_D0_%d_%d.yuv"%(j,i),
                                    resultPath+"rec_D1_1F/rec_D1_%d_%d.yuv"%(j,i),
                                    resultPath+"rec_D2_1F/rec_D2_%d_%d.yuv"%(j,i)])
    if not os.path.exists(resultPath+'rec_D0_1F'):
        os.makedirs(resultPath+'rec_D0_1F')
    listDecoderMdcConfig = [MDCDecoderLib.DecoderConfigFile(yuvOrgFileName=sequencePath+inputSrcFileName[0],reconD0FileName=resultPath+i[0],
                                                              reconD1FileName=resultPath+i[1],reconD2FileName=resultPath+i[2]) 
                                                              for i in listMDCFileName]
    listDecoderMdc = [MDCDecoderLib.DecoderMDC(i,pictureParam) for i in listDecoderMdcConfig]
    resultMDC = []
    with Pool() as p:
        resultMDC = p.map(workerMDC,listDecoderMdc)
    return resultMDC
def decodeSdc(pictureParam):
    listSDCFileName = []
    for i in range (0,51,1):
        listSDCFileName.append(resultPath+"rec_org_1F/rec_org_%d.yuv"%(i))
    listDecoderSdc = [MDCDecoderLib.DecoderSDC(sequencePath+i,sequencePath+inputSrcFileName[0],pictureParam) for i in listSDCFileName]
    resultSDC = []
    with Pool() as p:
        resultSDC = p.map(workerSDC,listDecoderSdc)
    return resultSDC
def exportDataAndPlot(resultSDC,resultMDC):
    sizeD1 = []
    sizeD2 = []
    listQP = []
    for i in range (5,51,5):
        for j in range (0,i,1):
            sizeD1.append(os.path.getsize(resultPath+"str_D1_1F/str_D1_%d_%d.hevc"%(j,i))*8)
            sizeD2.append(os.path.getsize(resultPath+"str_D2_1F/str_D2_%d_%d.hevc"%(j,i))*8)
            listQP.append([j,i])
    if not os.path.exists(resultPath+'csv/'):
        os.makedirs(resultPath+'csv')
    if not os.path.exists(resultPath+'csv/WithOutNoise'):
        os.makedirs(resultPath+'csv/WithOutNoise')
    PerformanceSDC = []
    for i,j in zip(range (0,51),resultSDC):
        PerformanceSDC.append([i,j[0],os.path.getsize(resultPath+"str_org_1F/str_org_%d.hevc"%(i))*8])
    PerformanceMDC = []
    for i,j,k,l in zip(listQP,resultMDC,sizeD1,sizeD2):
        PerformanceMDC.append([i[0],i[1],j[0],int (k)+int(l),j[1],int(k),j[2],int(l)])


    import pandas as pd
    dfMDC = pd.DataFrame(PerformanceMDC,
                         columns=["QP","QPM","PSNR0","R0(bits)","PSNR1","R1(bits)","PSNR2","R2(bits)"]
                         )
    dfMDC.to_csv(resultPath+"csv/WithOutNoise/Stat_MDC_CTUperSlice_1FH.csv",",",index=False)
    dfSDC = pd.DataFrame(PerformanceSDC,
                         columns=["QP","PSNR","R(bits)"])
    dfSDC.to_csv(resultPath+"csv/WithOutNoise/Stat_Encoder_CTUperSlice_1FH.csv",",",index=False)

    #convert to kbps 25 FPS
    dfSDC['R(Mbps)'] = dfSDC['R(bits)']/(352*288)
    dfMDC['R0(Mbps)'] = dfMDC['R0(bits)']/(352*288)

    import matplotlib.pyplot as plt
    plt.plot(dfSDC['R(Mbps)'],dfSDC['PSNR'],label="SDC/R")
    plt.plot(dfSDC['R(Mbps)']*2,dfSDC['PSNR'],label="SDC/2R")
    for d in dfMDC.groupby(dfMDC['QPM']):
        plt.scatter(d[1]['R0(Mbps)'],d[1]['PSNR0'],marker='+',label="QPM%d"%(d[0]))
    plt.xlabel("Rate(bpp)")
    plt.ylabel("PSNR (dB)")
    plt.legend(labelspacing=0.2,prop={'size':8})
    plt.show()
# runPoolEncoder()
# runPoolRefEncoder()
resultMDC = decodeMdc(pictureParam)
resultSDC = decodeSdc(pictureParam)
exportDataAndPlot(resultSDC,resultMDC)