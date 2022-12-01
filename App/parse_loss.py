#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 11:00:39 2022

@author: ubuntu
"""

import config
resultPath ="../result/"

#Open two File

class ParsingLoss:
    def __init__(self,filename):
        self.filename = filename
        self.tableFrameBlockLoss = [[]]
        self.POC = []
    def parse(self):
        with open(self.filename,"r") as file:
            for line in file:
                splitline = line.split(",")
                if (len(splitline)==1):
                    self.tableFrameBlockLoss.append([])
                    self.POC.append(int(splitline[0]))
                elif(len(splitline)==2):
                    self.tableFrameBlockLoss[len(self.tableFrameBlockLoss)-1].append([int (splitline[0]),int (splitline[1])])
    def getCTULossTable(self,POC):
        if POC in self.POC:
            pos = self.POC.index(POC)
            return self.tableFrameBlockLoss[pos]
        else:
            return []
            

description1 = ParsingLoss(resultPath+"debugD1.txt")
description1.parse()      
description2 = ParsingLoss(resultPath+"debugD2.txt")  
description2.parse()      

    