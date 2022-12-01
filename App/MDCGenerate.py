# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from functools import partial
from multiprocessing import Pool
import matplotlib.pyplot as plt
import os
import csv
from bitstring import BitStream
import os,glob,sys
import re
import config
sys.path.insert(0, '../Lib')
import HEVCInterfaceEncoder


outputFilePath = config.outputFilePath
mdcConfigPath = config.mdcConfigPath
sequencePath = config.sequencePath
resultPath = config.resultPath
libPath = config.libPath
QPPath = config.QPPath
listSeqCfgFileName = config.listSeqCfgFileName
listEncCfgD1FileName = config.listEncCfgD1FileName
listEncCfgD2FileName = config.listEncCfgD2FileName

nbFrame = config.nbFrame
QPstep = config.QPstep
QP_min = config.QP_min

QPMstep = config.QPMstep
QPM_min = config.QPM_min
QPM_max = config.QPM_max


def writeQPTestCaseHToFile(nbFrame,nbCTU,qpmin,qpmax):
    turn = 0
    with open (QPPath+"QP1_%d_%d.csv"%(qpmin,qpmax),"w") as qpfile1:
        with open(QPPath+"QP2_%d_%d.csv"%(qpmin,qpmax),"w") as qpfile2:
            for j in range (0,nbFrame):
                for i in range (0,nbCTU):
                    if (i%6==0):
                        turn = turn + 1
                    if (turn%2==0):
                        qpfile1.write("%d,\n"%(qpmin))
                        qpfile2.write("%d,\n"%(qpmax))
                    else:
                        qpfile1.write("%d,\n"%(qpmax))
                        qpfile2.write("%d,\n"%(qpmin))
def worker(obj):
    obj.runHEVCEncoderNoVerbose2()
def checkCompletedFile():
    origWD = os.getcwd()
    os.chdir(resultPath+"str_D1")
    regex = re.compile(r'\d+')
    listdoneD1=[]
    listdoneD2=[]
    for file in glob.glob("*.hevc"):
        listdoneD1.append(regex.findall(file))
    os.chdir(origWD)
    os.chdir(resultPath+"str_D2")
    for file in glob.glob("*.hevc"):
        listdoneD2.append(regex.findall(file))
    os.chdir(origWD)
    return listdoneD1,listdoneD2
def createObjList():
    listD1FileName = []
    listD2FileName = []
    listdoneD1,listdoneD2 = checkCompletedFile()
    dict_done_D1 ={}
    dict_done_D2={}
    for i in listdoneD1:
        dict_done_D1[(int(i[1]),int(i[2]))]=1
    for j in listdoneD2:
        dict_done_D2[int(j[1]),int(j[2])]=1

    for i in range (QPM_min,QPM_max,QPMstep):
        for j in range (QP_min,i,QPstep):
            if ((j,i) not in dict_done_D1):
                listD1FileName.append([resultPath+"str_D1/str_D1_%d_%d.hevc"%(j,i),resultPath+"rec_D1/rec_D1_%d_%d.yuv"%(j,i),QPPath+"QP1_%d_%d.csv"%(j,i),(i+j)/2])
            if ((j,i) not in dict_done_D2):
                listD2FileName.append([resultPath+"str_D2/str_D2_%d_%d.hevc"%(j,i),resultPath+"rec_D2/rec_D2_%d_%d.yuv"%(j,i),QPPath+"QP2_%d_%d.csv"%(j,i),(i+j)/2])
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
    for i in listEncoderHevcD1:
        list_worker.append(i)
    for j in listEncoderHevcD2:
            list_worker.append(j)
    with Pool() as p:
        p.map(worker,list_worker)

listD1FileName = []
listD2FileName = []
for i in range (QPM_min,QPM_max,QPMstep):
    for j in range (QP_min,i,QPstep):
        listD1FileName.append([resultPath+"str_D1/str_D1_%d_%d.hevc"%(j,i),resultPath+"rec_D1/rec_D1_%d_%d.yuv"%(j,i),QPPath+"QP1_%d_%d.csv"%(j,i),(i+j)/2])
        listD2FileName.append([resultPath+"str_D2/str_D2_%d_%d.hevc"%(j,i),resultPath+"rec_D2/rec_D2_%d_%d.yuv"%(j,i),QPPath+"QP2_%d_%d.csv"%(j,i),(i+j)/2])
        listEncoderHevcD1 = [HEVCInterfaceEncoder.HEVCEncoder(mdcConfigPath+listEncCfgD1FileName[0],
                                                      sequencePath+listSeqCfgFileName[0],
                                                      i[0],i[1],i[2],i[3]) for i in listD1FileName]
        listEncoderHevcD2 = [HEVCInterfaceEncoder.HEVCEncoder(mdcConfigPath+listEncCfgD2FileName[0],
                                                      sequencePath+listSeqCfgFileName[0],
                                                      i[0],i[1],i[2],i[3]) for i in listD2FileName]
list_worker = []
for i in listEncoderHevcD1:
    list_worker.append(i)
for j in listEncoderHevcD2:
    list_worker.append(j)
with Pool() as p:
    p.map(worker,list_worker)