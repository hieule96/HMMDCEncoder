#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 09:33:33 2022

@author: ubuntu
"""
import subprocess
import YUVLib
import Optimizer
import Quadtreelib as qd
import re
import numpy as np
import Optimizer as Opt
import sys
import skimage.metrics
import csv
import signal
from functools import partial
import pdb
import skimage.metrics
import os, errno
from math import log, e
import MDCDecoderLib
import HEVCInterfaceEncoder

class PictureParamter():
    def __init__(self,w,h,nbCUinCTU,frameToEncode):
        self.bord_h = h
        self.bord_w = w
        self.nbCUinCTU=nbCUinCTU
        self.frameToEncode = frameToEncode
        self.step_w = np.ceil(w/64)
        self.step_h = np.ceil(h/64)

ecoderHevcSdc = HEVCInterfaceEncoder.HEVCEncoder("outputs/qtree100.txt","MDC_cfg/encoder_intra_main.cfg","foreman_cif.cfg")
StatEncoder = []
fields=["QP","Rate(bits)","PSNRY","MSEY"]
pictureParam=PictureParamter(352,288,30,1)

for qp in range (0,51):
    bitrate,psnr_Y,mse_Y=ecoderHevcSdc.generateQtreeEncoderPSNRMSE(qp,"outputs/resi%d.yuv" %(qp),"outputs/qtree%d.txt"%(qp))
    list_element = []
    sizeOrg = os.path.getsize("str_org.hevc")
    DecoderSDC = MDCDecoderLib.DecoderSDC("rec_org.yuv", "foreman_cif.yuv", pictureParam)
    PSDC_mean,SDCPSNR_list = DecoderSDC.computePSNRSequence(0,300)
    StatEncoder.append([qp,sizeOrg*8,psnr_Y,mse_Y])
    
with open("Stat_Encoder_300F_CTUperSlice.csv","w") as file:
    writer = csv.writer(file)
    writer.writerow(fields)
    writer.writerows(StatEncoder)