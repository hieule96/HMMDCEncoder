#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 14:29:27 2022

@author: ubuntu
"""

import sys,os
sys.path.insert(0, '../Lib')
import YUVLib
import MDCDecoderLib
from os.path import join,getsize
import pandas as pd
from multiprocessing import Pool
import re
import yaml
from skimage.metrics import peak_signal_noise_ratio

hinted_path="../source/hinted"
org_path = "../source"
sequencePath = "../sequence/"

# Config file
if len(sys.argv) == 3:
    sequence = sys.argv[1]
    yamlFile = sys.argv[2]
else:
    sys.exit()
    print("Syntax Error: Decode-Noise-Ber.py sequence_name yaml_file")

D0PATH = join(hinted_path,sequence,"rec_D0_n")
SDCPATH = join(hinted_path,sequence,"rec_org_n")
OrgPATH = join(hinted_path,sequence,"rec_org_n")
list_mesure_MDC = []



with open(join("../source",yamlFile),"r") as yaml_stream:
    dict_sequence = yaml.safe_load(yaml_stream)
sequence_cfg = dict_sequence[sequence]
bord_w = sequence_cfg['w']
bord_h = sequence_cfg['h']
nbFrame = sequence_cfg['nbFrame']
pictureParam = MDCDecoderLib.PictureParamter(sequence_cfg['w'], sequence_cfg['h'], nbFrame)
pictureParam.nbFrame = nbFrame = sequence_cfg['nbFrame']

OrgPic = join(sequencePath,sequence_cfg['inputSrcFileName'])

D1_compressed = join(org_path,sequence,"str_D1")
D2_compressed = join(org_path,sequence,"str_D2")
MDC_D0_file = os.listdir(D0PATH)

def workerSDC(obj:MDCDecoderLib.DecoderSDC):
    print ("Compute SDC of %s %s %s\n" %(obj.orgFile,obj.outputFile,obj.pocFile))
    return obj.computePSNRwithmissing()


def computePSNRMDC(file):
    if file.endswith(".yuv"):
        e = re.split('\_|\.',file)
    QPp = int(e[3])
    QPr = int(e[4])
    psnr = 0
    print ("Compute PSNR of %s"%(file))
    for frame in range (0,nbFrame):
        imgMDC = YUVLib.read_YUV420_frame(open(join(D0PATH,file),"rb"),bord_w,bord_h,frame)
        imgO = YUVLib.read_YUV420_frame(open(join(sequencePath,OrgPic),"rb"),bord_w,bord_h,frame)
        psnr = psnr + peak_signal_noise_ratio(imgO._Y,imgMDC._Y,data_range=255)
        d1_size = getsize(join(D1_compressed,"str_D1_%s_%s.hevc"%(QPp,QPr)))
        d2_size = getsize(join(D2_compressed,"str_D2_%s_%s.hevc"%(QPp,QPr)))
    psnr_mean = psnr/nbFrame
    return QPp,QPr,d1_size,d2_size,d1_size+d2_size,psnr_mean

with Pool() as p:
    list_result_MDC = p.map(computePSNRMDC,MDC_D0_file)



listQPO = []
list_result_SDC = []
listDecoderSdcObj=[]
SDCPATH = join(hinted_path,sequence,"rec_org_n")
SDC_compressed = join(org_path,sequence,"str_org")
OrgPic = join(sequencePath,sequence_cfg['inputSrcFileName'])

for file in os.listdir(SDCPATH):
    if file.endswith(".yuv"):
        e = re.split('\_|\.',file)
        POCFile = "%s_%s_%s_%s.txt" %(e[0],e[1],e[2],e[3])
        sdc_size = getsize(join(SDC_compressed,"str_org_%s.hevc" %(e[3])))
        listDecoderSdcObj.append(MDCDecoderLib.DecoderSDC(OrgPic,
        pictureParam,
        int(e[3]),
        join(OrgPATH,POCFile),
        join(OrgPATH,file)))
        listQPO.append([e[3],sdc_size])
with Pool() as p:
    result_SDC = p.map(workerSDC,listDecoderSdcObj)
for k,l in zip(listQPO,result_SDC):
    list_result_SDC.append([l[1],k[1],l[0]])
    
dfSDC = pd.DataFrame(list_result_SDC,
                     columns=["QP","size","PSNR"])
dfMDC = pd.DataFrame(list_result_MDC,columns=["QPp","QPr","size1","size2","size","PSNR"])
dfSDC['size'] = (dfSDC['size']*8/(1_000_000*nbFrame))*30
dfMDC['size'] = (dfMDC['size']*8/(1_000_000*nbFrame))*30

import matplotlib.pyplot as plt
plt.scatter(dfSDC['size'],dfSDC['PSNR'],label="SDC")
for d in dfMDC.groupby(dfMDC['QPr']):
    plt.scatter(d[1]['size'],d[1]['PSNR'],marker='+',label="QPr%d"%(d[0]))
plt.xlabel("Rate Mbps")
plt.ylabel("EPSNR (dB)")
plt.title("Sequence %s with the %s of packet loss" %(sequence,dict_sequence['simulatorconfig']['pe']))
plt.legend()
plt.savefig("%s_%.3f_MDC_SDC.png" %(sequence,dict_sequence['simulatorconfig']['pe']))
plt.show()