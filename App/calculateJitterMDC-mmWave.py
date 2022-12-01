#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 17:18:01 2022

@author: ubuntu
"""

import pandas
import matplotlib.pyplot as plt
description1 = pandas.read_csv("../hinted/los1.txt",skiprows=9, sep='\t', index_col=False)
description2 = pandas.read_csv("../hinted/los2.txt",skiprows=9, sep='\t', index_col=False)
lastpacketRecept = pandas.concat([description1['L_ts'],description2['L_ts']],axis=1).max(axis=1)
lastpacketRecept = lastpacketRecept[:-2]
jitterMDC = lastpacketRecept - description1["F_ts"][:-2]
jitterMDC = jitterMDC.to_numpy()
jitterMDC = jitterMDC[jitterMDC>0]
plt.hist(jitterMDC)