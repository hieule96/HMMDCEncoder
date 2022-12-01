#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 14:45:48 2022

@author: ubuntu
"""
import config
import numpy as np
QPPath = config.QPPath
#cif resolution
# nbFrame = 50
# nbCTU = 30
# HD resolution
nbFrame = config.pictureParam.frameToEncode
nbCTU = config.pictureParam.nbCUinCTU
width = config.pictureParam.bord_w
height = config.pictureParam.bord_h
nbCTUperline = np.ceil(width/64)

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
                turn = 0
                for i in range (0,nbCTU):
                    if (i%nbCTUperline==0):
                        turn = turn + 1
                    if (turn%2==0):
                        qpfile1.write("%d,\n"%(qpmin))
                        qpfile2.write("%d,\n"%(qpmax))
                    else:
                        qpfile1.write("%d,\n"%(qpmax))
                        qpfile2.write("%d,\n"%(qpmin))
def writeQPTestCaseVToFile(nbFrame,nbCTU,qpmin,qpmax):
    with open (QPPath+"QP1_%d_%d.csv"%(qpmin,qpmax),"w") as qpfile1:
        with open(QPPath+"QP2_%d_%d.csv"%(qpmin,qpmax),"w") as qpfile2:
            for j in range (0,nbFrame):
                for i in range (0,nbCTU):
                    if (i%2==0):
                        qpfile1.write("%d,\n"%(qpmin))
                        qpfile2.write("%d,\n"%(qpmax))
                    else:
                        qpfile1.write("%d,\n"%(qpmax))
                        qpfile2.write("%d,\n"%(qpmin))
def writeQPTestCaseDToFile(nbFrame,nbCTU,qpmin,qpmax):
    with open (QPPath+"QP1_%d_%d.csv"%(qpmin,qpmax),"w") as qpfile1:
        with open(QPPath+"QP2_%d_%d.csv"%(qpmin,qpmax),"w") as qpfile2:
            for j in range (0,nbFrame):
                turn = 0
                for i in range (0,nbCTU):
                    if (i%width==0):
                        turn = turn + 1
                    if (turn%2==0):
                        if (i%2==0):
                            qpfile1.write("%d,\n"%(qpmin))
                            qpfile2.write("%d,\n"%(qpmax))
                        else:
                            qpfile1.write("%d,\n"%(qpmax))
                            qpfile2.write("%d,\n"%(qpmin))
                    else:
                        if (i%2==0):
                            qpfile2.write("%d,\n"%(qpmin))
                            qpfile1.write("%d,\n"%(qpmax))
                        else:
                            qpfile2.write("%d,\n"%(qpmax))
                            qpfile1.write("%d,\n"%(qpmin))
for i in range (QPM_min,QPM_max,QPMstep):
    for j in range (QP_min,i,QPstep):
        writeQPTestCaseHToFile(nbFrame,nbCTU,j,i)

# writeQPTestCaseHToFile(300,30,26,48)