#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 15:19:01 2022

@author: ubuntu
"""

import sys,os
sys.path.insert(0, '../Lib/')
import MDCDecoderLib
from bjontegaard_metric import *
from multiprocessing import Pool
from os import listdir,makedirs
from os.path import isfile, join, exists, getsize
import re
import pandas as pd
import yaml
hinted_path="../source/hinted"
org_path = "../source"


file_D1 = "../result/rec_D1.yuv"
file_D2 = "../result/rec_D2.yuv"
file_D0 = "../result/rec_D0.yuv"
OrgPic="../sequence/ParkScene_1920x1080_24.yuv"


pictureParam = MDCDecoderLib.PictureParamter(1920,1080,24)
decoderCfg = MDCDecoderLib.DecoderMDCConfigFile(OrgPic,
                                    file_D0,
                                    file_D1,
                                    file_D2,
                                    24,
                                    50,
                                    "",
                                    "",
                                    "")
dec = MDCDecoderLib.DecoderMDC(decoderCfg, pictureParam)
x = dec.merge2Frame8x8(0, 23)