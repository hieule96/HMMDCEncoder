#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 14:05:37 2022

@author: ubuntu
"""

import pandas as pd
import matplotlib.pyplot as plt
import config
dfSDC1 = pd.read_csv(config.resultPath+"csv/NoNoise/Stat_Encoder_CTUperSlice_300FD.csv")
dfMDC1 = pd.read_csv(config.resultPath+"csv/NoNoise/Stat_MDC_CTUperSlice_300FD.csv")

dfSDC2 = pd.read_csv(config.resultPath+"csv/NoNoise/Stat_Encoder_CTUperSlice_300FH.csv")
dfMDC2 = pd.read_csv(config.resultPath+"csv/NoNoise/Stat_MDC_CTUperSlice_300FH.csv")

dfSDC3 = pd.read_csv(config.resultPath+"csv/NoNoise/Stat_Encoder_CTUperSlice_300FV.csv")
dfMDC3 = pd.read_csv(config.resultPath+"csv/NoNoise/Stat_MDC_CTUperSlice_300FV.csv")

dfSDC1['R(Mbps)'] = (dfSDC1['R(bits)']/1_000_000)*(25/config.nbFrame)
dfMDC1['R0(Mbps)'] = (dfMDC1['R0(bits)']/1_000_000)*(25/config.nbFrame)

dfSDC2['R(Mbps)'] = (dfSDC2['R(bits)']/1_000_000)*(25/config.nbFrame)
dfMDC2['R0(Mbps)'] = (dfMDC2['R0(bits)']/1_000_000)*(25/config.nbFrame)
dfSDC3['R(Mbps)'] = (dfSDC3['R(bits)']/1_000_000)*(25/config.nbFrame)
dfMDC3['R0(Mbps)'] = (dfMDC3['R0(bits)']/1_000_000)*(25/config.nbFrame)

list_marker = ["v","2",'h',"D","s"]
colors = ["y","r","c","g","maroon"]
plt.plot(dfSDC1['R(Mbps)'],dfSDC1['PSNR'],label="SDC/R",marker="+")
plt.plot(dfSDC1['R(Mbps)']*2,dfSDC1['PSNR'],label="SDC/2R",marker=".")
for d,mark,color in zip(dfMDC1.groupby(dfMDC1['QPM']),list_marker,colors):
        plt.plot(d[1]['R0(Mbps)'],d[1]['PSNR0'],label="$QP_{r}:%d$"%(d[0]),marker=mark,color=color)
plt.xlabel("Rate(Mbps)")
plt.ylabel("E[PSNR_Y] (dB)")
plt.legend(labelspacing=0.2,prop={'size':11})
plt.grid(True)
plt.show()


plt.plot(dfSDC2['R(Mbps)'],dfSDC2['PSNR'],label="SDC/R",marker="+")
plt.plot(dfSDC2['R(Mbps)']*2,dfSDC2['PSNR'],label="SDC/2R",marker=".")
for d,mark,color in zip(dfMDC2.groupby(dfMDC2['QPM']),list_marker,colors):
        plt.plot(d[1]['R0(Mbps)'],d[1]['PSNR0'],label="$QP_{r}:%d$"%(d[0]),marker=mark,color=color)
plt.xlabel("Rate(Mbps)")
plt.ylabel("E[PSNR_Y] (dB)")
plt.legend(labelspacing=0.2,prop={'size':11})
plt.grid(True)
plt.show()

plt.plot(dfSDC3['R(Mbps)'],dfSDC3['PSNR'],label="SDC/R",marker="+")
plt.plot(dfSDC3['R(Mbps)']*2,dfSDC3['PSNR'],label="SDC/2R",marker=".")
for d,mark,color in zip(dfMDC3.groupby(dfMDC3['QPM']),list_marker,colors):
        plt.plot(d[1]['R0(Mbps)'],d[1]['PSNR0'],label="$QP_{r}:%d$"%(d[0]),marker=mark,color=color)
plt.xlabel("Rate(Mbps)")
plt.ylabel("E[PSNR_Y] (dB)")
plt.legend(labelspacing=0.2,prop={'size':11})
plt.grid(True)
plt.show()
