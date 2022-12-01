#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 12:46:50 2022

@author: ubuntu
"""

import pandas as pd
import matplotlib.pyplot as plt
import config
from bj_delta import *

# dfSDC = pd.read_csv(config.resultPath+"csv/WithNoiseClearPoints/Stat_Encoder_pedestrian_area_1080p25.yuv_100FH_0.050.csv")
# dfMDC = pd.read_csv(config.resultPath+"csv/WithNoiseClearPoints/Stat_MDC_pedestrian_area_1080p25.yuv_noise_100FH_0.050.csv")
# dfSDC1 = pd.read_csv(config.resultPath+"csv/WithNoiseBestPerformance/Stat_Encoder_foreman_cif.yuv_300FH_0.200.csv")
# dfMDC1 = pd.read_csv(config.resultPath+"csv/WithNoiseBestPerformance/Stat_MDC_foreman_cif.yuv_noise_300FH_0.200.csv")
# dfSDC2 = pd.read_csv(config.resultPath+"csv/WithNoiseBestPerformance/Stat_Encoder_foreman_cif.yuv_300FH_0.150.csv")
# dfMDC2 = pd.read_csv(config.resultPath+"csv/WithNoiseBestPerformance/Stat_MDC_foreman_cif.yuv_noise_300FH_0.150.csv")
# dfSDC3 = pd.read_csv(config.resultPath+"csv/WithNoiseBestPerformance/Stat_Encoder_foreman_cif.yuv_300FH_0.100.csv")
# dfMDC3 = pd.read_csv(config.resultPath+"csv/WithNoiseBestPerformance/Stat_MDC_foreman_cif.yuv_noise_300FH_0.100.csv")
# dfSDC4 = pd.read_csv(config.resultPath+"csv/WithNoiseBestPerformance/Stat_Encoder_foreman_cif.yuv_300FH_0.050.csv")
# dfMDC4 = pd.read_csv(config.resultPath+"csv/WithNoiseBestPerformance/Stat_MDC_foreman_cif.yuv_noise_300FH_0.050.csv")
# #convert to kbps 25 FPS
# dfSDC1['R(Mbps)'] = (dfSDC1['R(bits)']/1_000_000)*(25/config.nbFrame)
# dfMDC1['R0(Mbps)'] = (dfMDC1['R0(bits)']/1_000_000)*(25/config.nbFrame)

# dfSDC2['R(Mbps)'] = (dfSDC2['R(bits)']/1_000_000)*(25/config.nbFrame)
# dfMDC2['R0(Mbps)'] = (dfMDC2['R0(bits)']/1_000_000)*(25/config.nbFrame)
# dfSDC3['R(Mbps)'] = (dfSDC3['R(bits)']/1_000_000)*(25/config.nbFrame)
# dfMDC3['R0(Mbps)'] = (dfMDC3['R0(bits)']/1_000_000)*(25/config.nbFrame)
# dfSDC4['R(Mbps)'] = (dfSDC4['R(bits)']/1_000_000)*(25/config.nbFrame)
# dfMDC4['R0(Mbps)'] = (dfMDC4['R0(bits)']/1_000_000)*(25/config.nbFrame)
# plt.plot(dfSDC['R(Mbps)'],dfSDC['PSNR'],label="SDC/R",marker="+")
# list_marker = ["v","2",'h',"D","s"]
# for d,mark in zip(dfMDC.groupby(dfMDC['QPM']),list_marker):
#         plt.plot(d[1]['R0(Mbps)'],d[1]['PSNR0'],label="QPM%d"%(d[0]),marker=mark)
# plt.xlabel("Rate(Mbps)")
# plt.ylabel("E[PSNR] [dB]")
# plt.legend(labelspacing=0.2,prop={'size':8})
# plt.show()

# plt.plot(dfSDC1['R(Mbps)'],dfSDC1['PSNR'],label="SDC 20%",marker="v",linestyle='dashed')
# plt.plot(dfMDC1['R0(Mbps)'],dfMDC1['PSNR0'],label="MDC 20%",marker="v")

# plt.plot(dfSDC2['R(Mbps)'],dfSDC2['PSNR'],label="SDC 15%",marker="d",linestyle='dashed')
# plt.plot(dfMDC2['R0(Mbps)'],dfMDC2['PSNR0'],label="MDC 15%",marker="d")
# plt.plot(dfSDC3['R(Mbps)'],dfSDC3['PSNR'],label="SDC 10%",marker="H",linestyle='dashed')
# plt.plot(dfMDC3['R0(Mbps)'],dfMDC3['PSNR0'],label="MDC 10%",marker="H")
# plt.plot(dfSDC4['R(Mbps)'],dfSDC4['PSNR'],label="SDC 5%",marker="^",linestyle='dashed')
# plt.plot(dfMDC4['R0(Mbps)'],dfMDC4['PSNR0'],label="MDC 5 %",marker="^")
# plt.xlabel("Rate(Mbps)")
# plt.ylabel("E[PSNR_Y] (dB)")
# plt.rc('grid', linestyle="dashed", color='black')
# plt.grid(True)
# plt.legend(labelspacing=0.2,prop={'size':10},ncol=4,bbox_to_anchor=(1.0,-0.2))
# plt.show()

# bd_psnr1 = bj_delta(dfSDC1['R(Mbps)'],dfSDC1['PSNR'],dfMDC1['R0(Mbps)'],dfMDC1['PSNR0'],1)
# bd_psnr2 = bj_delta(dfSDC2['R(Mbps)'],dfSDC2['PSNR'],dfMDC2['R0(Mbps)'],dfMDC2['PSNR0'],1)
# bd_psnr3 = bj_delta(dfSDC3['R(Mbps)'],dfSDC3['PSNR'],dfMDC3['R0(Mbps)'],dfMDC3['PSNR0'],1)
# bd_psnr4 = bj_delta(dfSDC4['R(Mbps)'],dfSDC4['PSNR'],dfMDC4['R0(Mbps)'],dfMDC4['PSNR0'],1)

dfSDC1 = pd.read_csv(config.resultPath+"csv/WithNoiseClearPoints/Stat_Encoder_foreman_cif.yuv_300FH_0.200.csv")
dfMDC1 = pd.read_csv(config.resultPath+"csv/WithNoiseClearPoints/Stat_MDC_foreman_cif.yuv_noise_300FH_0.200.csv")
dfSDC2 = pd.read_csv(config.resultPath+"csv/WithNoiseClearPoints/Stat_Encoder_foreman_cif.yuv_300FH_0.150.csv")
dfMDC2 = pd.read_csv(config.resultPath+"csv/WithNoiseClearPoints/Stat_MDC_foreman_cif.yuv_noise_300FH_0.150.csv")
dfSDC3 = pd.read_csv(config.resultPath+"csv/WithNoiseClearPoints/Stat_Encoder_foreman_cif.yuv_300FH_0.100.csv")
dfMDC3 = pd.read_csv(config.resultPath+"csv/WithNoiseClearPoints/Stat_MDC_foreman_cif.yuv_noise_300FH_0.100.csv")
dfSDC4 = pd.read_csv(config.resultPath+"csv/WithNoiseClearPoints/Stat_Encoder_foreman_cif.yuv_300FH_0.050.csv")
dfMDC4 = pd.read_csv(config.resultPath+"csv/WithNoiseClearPoints/Stat_MDC_foreman_cif.yuv_noise_300FH_0.050.csv")

dfSDC1['R(Mbps)'] = (dfSDC1['R(bits)']/1_000_000)*(25/config.nbFrame)
dfMDC1['R0(Mbps)'] = (dfMDC1['R0(bits)']/1_000_000)*(25/config.nbFrame)

dfSDC2['R(Mbps)'] = (dfSDC2['R(bits)']/1_000_000)*(25/config.nbFrame)
dfMDC2['R0(Mbps)'] = (dfMDC2['R0(bits)']/1_000_000)*(25/config.nbFrame)
dfSDC3['R(Mbps)'] = (dfSDC3['R(bits)']/1_000_000)*(25/config.nbFrame)
dfMDC3['R0(Mbps)'] = (dfMDC3['R0(bits)']/1_000_000)*(25/config.nbFrame)
dfSDC4['R(Mbps)'] = (dfSDC4['R(bits)']/1_000_000)*(25/config.nbFrame)
dfMDC4['R0(Mbps)'] = (dfMDC4['R0(bits)']/1_000_000)*(25/config.nbFrame)

plt.plot(dfSDC1['R(Mbps)'],dfSDC1['PSNR'],label="SDC/R",marker="+")
list_marker = ["v","2",'h',"D","s"]
for d,mark in zip(dfMDC1.groupby(dfMDC1['QPM']),list_marker):
        plt.plot(d[1]['R0(Mbps)'],d[1]['PSNR0'],label="QPM%d"%(d[0]),marker=mark)
plt.xlabel("Rate(Mbps)")
plt.ylabel("E[PSNR] [dB]")
plt.legend(labelspacing=0.2,prop={'size':8})
plt.rc('grid', linestyle="dashed", color='black')
plt.grid(True)
plt.show()

plt.plot(dfSDC2['R(Mbps)'],dfSDC2['PSNR'],label="SDC/R",marker="+")
list_marker = ["v","2",'h',"D","s"]
for d,mark in zip(dfMDC2.groupby(dfMDC2['QPM']),list_marker):
        plt.plot(d[1]['R0(Mbps)'],d[1]['PSNR0'],label="QPM%d"%(d[0]),marker=mark)
plt.xlabel("Rate(Mbps)")
plt.ylabel("E[PSNR] [dB]")
plt.legend(labelspacing=0.2,prop={'size':8})
plt.rc('grid', linestyle="dashed", color='black')
plt.grid(True)
plt.show()

plt.plot(dfSDC3['R(Mbps)'],dfSDC3['PSNR'],label="SDC/R",marker="+")
list_marker = ["v","2",'h',"D","s"]
for d,mark in zip(dfMDC3.groupby(dfMDC3['QPM']),list_marker):
        plt.plot(d[1]['R0(Mbps)'],d[1]['PSNR0'],label="QPM%d"%(d[0]),marker=mark)
plt.xlabel("Rate(Mbps)")
plt.ylabel("E[PSNR] [dB]")
plt.legend(labelspacing=0.2,prop={'size':8})
plt.rc('grid', linestyle="dashed", color='black')
plt.grid(True)
plt.show()

plt.plot(dfSDC4['R(Mbps)'],dfSDC4['PSNR'],label="SDC/R",marker="+")
list_marker = ["v","2",'h',"D","s"]
for d,mark in zip(dfMDC4.groupby(dfMDC4['QPM']),list_marker):
        plt.plot(d[1]['R0(Mbps)'],d[1]['PSNR0'],label="QPM%d"%(d[0]),marker=mark)
plt.xlabel("Rate(Mbps)")
plt.ylabel("E[PSNR] [dB]")
plt.legend(labelspacing=0.2,prop={'size':8})
plt.rc('grid', linestyle="dashed", color='black')
plt.grid(True)
plt.show()

