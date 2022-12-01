#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:41:42 2022

@author: ubuntu
"""
# import sys
# sys.path.insert(0, '../Lib')
# import MDCDecoderLib

# outputFilePath = "../outputs/"
# mdcConfigPath = "../MdcCfgns/"
# sequencePath = "../sequence/"
# resultPath ="../result/"
# libPath = "../Lib/"
# QPPath = "../QP/"
# inputSrcFileName = ["soccer_cif.yuv"]
# listSeqCfgFileName = ["soccer_cif.cfg"]
# listEncCfgD1FileName = ["encoder_intra_main-D1.cfg"]
# listEncCfgD2FileName = ["encoder_intra_main-D2.cfg"]
# listPOCD1Noise = ["POC1noise.txt"]
# listPOCD2Noise = ["POC2noise.txt"]
# nbFrame = 300
# pictureParam = MDCDecoderLib.PictureParamter(352, 288, 30, nbFrame)
# #Noise parameter
# p = 0.10
# r = 1.0
# iteration = 5
# #config refencoder
# listEncCfgorgFileName = ["encoder_intra_main.cfg"]

# QPstep = 3
# QP_min = 12

# QPMstep = 10
# QPM_min = 20
# QPM_max = 51

# import sys
# sys.path.insert(0, '../Lib')
# import MDCDecoderLib

# # Config for HD stream
# outputFilePath = "../outputs/"
# mdcConfigPath = "../MdcCfgns/"
# sequencePath = "../sequence/"
# resultPath ="../result/"
# libPath = "../Lib/"
# QPPath = "../QP/"
# inputSrcFileName = ["pedestrian_area_1080p25.yuv"]
# listSeqCfgFileName = ["pedestrian_area.cfg"]
# listEncCfgD1FileName = ["encoder_intra_main-D1.cfg"]
# listEncCfgD2FileName = ["encoder_intra_main-D2.cfg"]
# listPOCD1Noise = ["POC1noise.txt"]
# listPOCD2Noise = ["POC2noise.txt"]
# nbFrame = 100
# pictureParam = MDCDecoderLib.PictureParamter(1920, 1080, 510, nbFrame)
# #Noise parameter
# p = 0.20
# r = 1.0
# iteration = 5
# #config refencoder
# listEncCfgorgFileName = ["encoder_intra_main.cfg"]

# QPstep = 3
# QP_min = 12

# QPMstep = 10
# QPM_min = 20
# QPM_max = 51


# import sys
# sys.path.insert(0, '../Lib')
# import MDCDecoderLib

# # Config for HD stream
# outputFilePath = "../outputs/"
# mdcConfigPath = "../MdcCfgns/"
# sequencePath = "../sequence/"
# resultPath ="../result/"
# libPath = "../Lib/"
# QPPath = "../QP/"
# inputSrcFileName = ["rush_hour_1080p25.yuv"]
# listSeqCfgFileName = ["rush_hour_1080p25.cfg"]
# listEncCfgD1FileName = ["encoder_intra_main-D1.cfg"]
# listEncCfgD2FileName = ["encoder_intra_main-D2.cfg"]
# listPOCD1Noise = ["POC1noise.txt"]
# listPOCD2Noise = ["POC2noise.txt"]
# nbFrame = 100
# pictureParam = MDCDecoderLib.PictureParamter(1920, 1080, 510, nbFrame)
# #Noise parameter
# p = 0.15
# r = 1.0
# iteration = 5
# #config refencoder
# listEncCfgorgFileName = ["encoder_intra_main.cfg"]

# QPstep = 3
# QP_min = 18

# QPMstep = 10
# QPM_min = 30
# QPM_max = 51

import sys
sys.path.insert(0, '../Lib')
import MDCDecoderLib

# # Config for HD stream
# outputFilePath = "../outputs/"
# mdcConfigPath = "../MdcCfgns/"
# sequencePath = "../sequence/"
# resultPath ="../result/"
# libPath = "../Lib/"
# QPPath = "../QP/"
# inputSrcFileName = ["deadline_cif.yuv"]
# listSeqCfgFileName = ["deadline_cif.cfg"]
# listEncCfgD1FileName = ["encoder_intra_main-D1.cfg"]
# listEncCfgD2FileName = ["encoder_intra_main-D2.cfg"]
# listPOCD1Noise = ["POC1noise.txt"]
# listPOCD2Noise = ["POC2noise.txt"]
# nbFrame = 300
# pictureParam = MDCDecoderLib.PictureParamter(352, 288, 30, nbFrame)
# #Noise parameter
# p = 0.15
# r = 1.0
# iteration = 5
# #config refencoder
# listEncCfgorgFileName = ["encoder_intra_main.cfg"]

# QPstep = 3
# QP_min = 18

# QPMstep = 10
# QPM_min = 30
# QPM_max = 51

# # Forman
# outputFilePath = "../outputs/"
# mdcConfigPath = "../MdcCfgns/"
# sequencePath = "../sequence/"
# resultPath ="../result/"
# libPath = "../Lib/"
# QPPath = "../QP/"
# inputSrcFileName = ["foreman_cif.yuv"]
# listSeqCfgFileName = ["foreman_cif.cfg"]
# listEncCfgD1FileName = ["encoder_intra_main-D1.cfg"]
# listEncCfgD2FileName = ["encoder_intra_main-D2.cfg"]
# listPOCD1Noise = ["POC1noise.txt"]
# listPOCD2Noise = ["POC2noise.txt"]
# nbFrame = 300
# pictureParam = MDCDecoderLib.PictureParamter(352, 288, 30, nbFrame)
# #Noise parameter
# p = 0.15
# r = 1.0
# iteration = 5
# #config refencoder
# listEncCfgorgFileName = ["encoder_intra_main.cfg"]

# QPstep = 3
# QP_min = 18

# QPMstep = 10
# QPM_min = 30
# QPM_max = 51

# Forman
outputFilePath = "../outputs/"
mdcConfigPath = "../MdcCfgns/"
sequencePath = "../sequence/"
resultPath ="../result/"
libPath = "../Lib/"
QPPath = "../QP/"
inputSrcFileName = ["soccer_cif.yuv"]
listSeqCfgFileName = ["soccer.cfg"]
listEncCfgD1FileName = ["encoder_intra_main-D1.cfg"]
listEncCfgD2FileName = ["encoder_intra_main-D2.cfg"]
listPOCD1Noise = ["POC1noise.txt"]
listPOCD2Noise = ["POC2noise.txt"]
nbFrame = 300
pictureParam = MDCDecoderLib.PictureParamter(352, 288, 30, nbFrame)
#Noise parameter
p = 0.15
r = 1.0
iteration = 5
#config refencoder
listEncCfgorgFileName = ["encoder_intra_main.cfg"]

QPstep = 3
QP_min = 18

QPMstep = 10
QPM_min = 30
QPM_max = 51
