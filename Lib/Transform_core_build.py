#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 11:54:18 2021

@author: ubuntu
"""

import numpy as np
import scipy.fft as fft


# def dct_funct(i,j):
#     return (1/np.sqrt(4))*np.cos((np.pi/4)*(j+(1/2))*i)
# def writenpArrayToFile(YUVArray,outputFileName,mode='wb'):
#     with open(outputFileName,mode) as output:
#         output.write(YUVArray[0].tobytes())
#         output.write(YUVArray[1].tobytes())
#         output.write(YUVArray[2].tobytes())
# XTess = np.full((4,4),-127)
# XTess2 = np.full((16,16),-127)

# A = np.full((4, 4), np.sqrt(2))
# A[:,0] = 1
# TF_mat = np.fromfunction(dct_funct,(4,4))*A

# dct_vector_unique = [90,90,90,89,88,87,85,83,82,
#                      80,78,75,73,70,67,64,61,57,
#                      54,50,46,43,38,36,31,25,22,
#                      18,13,9,4]

# D = [[64,64,64,64],
#      [83,36,-36,-83],
#      [64,-64,-64,64],
#      [36,-83,83,-36]]

# YUVJoint = [[],[],[]]
# YUVJoint[0] = np.ones((352,288),dtype=np.uint8)
# YUVJoint[1] = np.ones((352,288),dtype=np.uint8)
# YUVJoint[2] = np.ones((352,288),dtype=np.uint8)

# writenpArrayToFile(YUVJoint,"Echelon.yuv")

# dct = fft.dct(fft.dct(XTess2.T, type=2, norm = 'backward').T, type=2, norm = 'backward')
# D = np.array(D,dtype=int)
# T1D = D.dot(XTess) >> 1
# T2D = T1D.dot(D.T) >> 9
# dct2=T2D

def dst4x4_matrix(a,b,c,d):
    array = [[a,b,c,d],[c,c,0,-c],[d,-a,-c,b],[b,-d,c,a]]
    return np.array(array,dtype=int)

T_dst4x4 = dst4x4_matrix(29, 55, 74, 84)

