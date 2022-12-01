#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:08:55 2022

@author: ubuntu
"""

import pandas
import matplotlib.pyplot as plt
H264 = pandas.read_csv("../hinted/ComparisionHEVC264/loss_264.txt",skiprows=6, sep='\t', index_col=False)
H265 = pandas.read_csv("../hinted/ComparisionHEVC264/loss_265.txt",skiprows=9, sep='\t', index_col=False)
jitter1 = H264[H264['jit'] > 0]['jit']
jitter2 = H265[H265['jit'] > 0]['jit']
plt.hist(jitter1)
plt.show()
plt.hist(jitter2)
plt.show()