#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:47:08 2022

@author: ubuntu
"""

"""
Simulate the loss by generating the TX RX files
"""
import logging,sys
sys.path.insert(0, '../Lib')
import MarkovChain
from os import listdir,makedirs
from os.path import isfile, join, exists
import yaml
TRACEPATH = "../source/trace"
TXRXPATH = "../source/TXRX"
def convertToInt(s):
    try:
        return int (s)
    except ValueError:
        logging.warning("Value error")
        return s
class PLRProcess():
    def __init__(self,initial_state:MarkovChain.ChannelState,p:float,r:float):
        states = [MarkovChain.ChannelState.GOOD, MarkovChain.ChannelState.BAD]
        transition_matrix= [[1 - p, p], [r, 1 - r]]
        self.ChannelSim = MarkovChain.MarkovChain(transition_matrix, states)
        self.actual_state = initial_state
    def getnextState(self):
        self.actual_state = self.ChannelSim.next_state(self.actual_state)
    def getActualState(self):
        return self.actual_state
    
def GenerateTXRXFile(tracefile:str,txfile:str,rxfile:str,randomprocess:PLRProcess):
    print ("[PLR-Noise] Generating %s %s"%(txfile,rxfile))
    with open(tracefile,"r") as tracefile:
        with open(txfile,"w") as txfile:
            with open(rxfile,"w") as rxfile:
                for lines in tracefile:
                    token = lines.split(sep="\t")
                    txfile.write("%d,udp,%d,%d\n" %(convertToInt(token[0])-1,convertToInt(token[3]),convertToInt(token[2])))
                    if randomprocess.getActualState() == MarkovChain.ChannelState.GOOD:
                        rxfile.write("%d,udp,%d,%d\n" %(convertToInt (token[0])-1,convertToInt (token[3]),convertToInt (token[2])))
                    randomprocess.getnextState()
                    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        TRACEPATH = join(TRACEPATH,sys.argv[1])
        TXRXPATH = join(TXRXPATH, sys.argv[1])
        yamlFile = sys.argv[2]
    else:
        print("WARNING: No specific folder and PLR is set for the output file")
        sys.exit()
    with open(join("../source",yamlFile),"r") as yaml_stream:
    	dict_sequence = yaml.safe_load(yaml_stream)
    plr = float (dict_sequence['simulatorconfig']['pe'])
    print ("PLR",plr)
    makedirs(TRACEPATH,exist_ok=True)
    makedirs(TXRXPATH,exist_ok=True)
    tracefile = [f for f in listdir(TRACEPATH) if isfile(join(TRACEPATH,f))]
    if (len (tracefile) ==0):
        print ("No file in the folder")
        sys.exit()
    if (not exists(TXRXPATH)):
        makedirs(TXRXPATH)
    for trace in tracefile:
        process = PLRProcess(MarkovChain.ChannelState.GOOD, plr, 1)
        GenerateTXRXFile(join(TRACEPATH,trace),join(TXRXPATH,"TX_%s.txt" %(trace)),join(TXRXPATH,"RX_%s.txt" %(trace)),process)
