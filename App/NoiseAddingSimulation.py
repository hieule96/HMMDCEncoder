#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 16:51:05 2022

@author: ubuntu
"""

from functools import partial
import os,sys,glob
from bitstring import BitStream
import re
sys.path.insert(0, '../Lib')
import MarkovChain
import NALUnitProcessing as nal
import config


outputFilePath = config.outputFilePath
mdcConfigPath = config.mdcConfigPath
sequencePath = config.sequencePath
resultPath = config.resultPath
libPath = config.libPath
QPPath = config.QPPath


iteration = config.iteration
listBitStreamD1FileName = []
listBitStreamD2FileName = []
listBitStreamOrgFileName = []

p = config.p
r = config.r

QPstep = config.QPstep
QP_min = config.QP_min

QPMstep = config.QPMstep
QPM_min = config.QPM_min
QPM_max = config.QPM_max

def addNoiseToSignal(orgFile, noiseFile, initstate=MarkovChain.ChannelState.GOOD, p=0.01, r=1.0,iteration = 4):
    # Noise config
    initial_state = initstate
    states = [MarkovChain.ChannelState.GOOD, MarkovChain.ChannelState.BAD]
    transition_matrix1 = [[1 - p, p], [r, 1 - r]]
    ChannelSim = MarkovChain.MarkovChain(transition_matrix1, states)
    for it in range (0,iteration):
       filename,ext = os.path.splitext(noiseFile)
       with open(orgFile, "rb") as original_stream:
            with open(filename+"_%d"%(it)+ext, "wb") as noise_stream:
                for chunk in iter(partial(original_stream.read, 1500), b''):
                    if (initial_state == MarkovChain.ChannelState.GOOD):
                        noise_stream.write(chunk)
                    initial_state = ChannelSim.next_state(initial_state)


def addNoiseToSignalNAL3(orgFile, noiseFile, initstate=MarkovChain.ChannelState.GOOD, p=0.01, r=1.0,iteration = 4):
    # Noise config
    initial_state = initstate
    states = [MarkovChain.ChannelState.GOOD, MarkovChain.ChannelState.BAD]
    transition_matrix= [[1 - p, p], [r, 1 - r]]
    ChannelSim = MarkovChain.MarkovChain(transition_matrix, states)
    # bitstream
    stream = BitStream(filename=orgFile)
    nals = list(stream.findall('0x000001', bytealigned=True))
    size = [y - x for x, y in zip(nals, nals[1:])]
    size.append(stream.length - 1 - nals[-1])
    # Last NAL size
    number_packet_loss = []
    nal_loss = []
    for it in range (0,iteration):
        stream.pos = 0
        filename,ext = os.path.splitext(noiseFile)
        count_loss = 0
        count_packet = 0
        with open(filename+"_%d"%(it)+ext, "wb") as noise_stream:
            for i, n in zip(nals, size):
                saved_pos = stream.pos
                addNoise = nal.read_nal_unit(stream, i, n // 8)
                endPos = stream.pos
                stream.pos = saved_pos
                if addNoise:
                    if (initial_state == MarkovChain.ChannelState.GOOD):
                        nal.write_nal_units(stream, i, n // 8, noise_stream)
                    else:
                        noise_stream.write(stream.read('bytes:3'))
                        stream.pos = endPos
                        count_loss = count_loss + 1
                        nal_loss.append(count_packet)
                    initial_state = ChannelSim.next_state(initial_state)
                else:
                    nal.write_nal_units(stream, i, n // 8, noise_stream)
                count_packet = count_packet + 1
        number_packet_loss.append(count_loss)
    return number_packet_loss,nal_loss

def addNoiseToSignalNAL(orgFile, noiseFile, initstate=MarkovChain.ChannelState.GOOD, p=0.01, r=1.0):
    # Noise config
    initial_state = initstate
    states = [MarkovChain.ChannelState.GOOD, MarkovChain.ChannelState.BAD]
    transition_matrix1 = [[1 - p, p], [r, 1 - r]]
    ChannelSim = MarkovChain.MarkovChain(transition_matrix1, states)
    # check NAL
    countzeros = 0
    countNAL = 0
    isNAL = False
    isWrite = False
    pos = 0
    with open(orgFile, "rb") as original_stream:
        with open(noiseFile, "wb") as noise_stream:
            for chunk in iter(partial(original_stream.read, 1), b''):
                pos = pos + 1
                # Detect NAL separator to scramble
                if (chunk == bytearray([int('0x01', 16)]) and countzeros == 2):
                    countzeros = 0
                    isNAL = True
                    countNAL = countNAL + 1
                # skipped header
                elif (chunk == bytearray([int('0x01', 16)]) and countzeros == 3):
                    countzeros = 0
                    isNAL = False
                    if isWrite == False:
                        isWrite = True
                        noise_stream.write(bytearray([int('0x00', 16), int('0x00', 16), int('0x00', 16)]))
                # Detect the begin code
                elif chunk == bytearray([int('0x00', 16)]):
                    countzeros = countzeros + 1
                # Reset the signal
                else:
                    countzeros = 0

                # change State
                if (isNAL):
                    if (initial_state == MarkovChain.ChannelState.GOOD):
                        isWrite = True
                        if (isWrite == False):
                            noise_stream.write(bytearray([int('0x00', 16), int('0x00', 16)]))
                    else:
                        isWrite = False
                    initial_state = ChannelSim.next_state(initial_state)
                    isNAL = False
                if (isWrite):
                    noise_stream.write(chunk)
        print(countNAL)


def addNoiseToSignalNAL2(orgFile, noiseFile, initstate=MarkovChain.ChannelState.GOOD, p=0.01, r=0.9):
    # Noise config
    initial_state = initstate
    states = [MarkovChain.ChannelState.GOOD, MarkovChain.ChannelState.BAD]
    transition_matrix1 = [[1 - p, p], [r, 1 - r]]
    ChannelSim = MarkovChain.MarkovChain(transition_matrix1, states)
    # check NAL
    countzeros = 0
    countNAL = 0
    isNAL = False
    isHeader = False
    pos = 0
    with open(orgFile, "rb") as original_stream:
        with open(noiseFile, "wb") as noise_stream:
            for chunk in iter(partial(original_stream.read, 1), b''):
                pos = pos + 1
                # Detect NAL separator
                if (chunk == bytearray([int('0x01', 16)]) and countzeros == 2):
                    countzeros = 0
                    isNAL = True
                    isHeader = False
                    countNAL = countNAL + 1
                elif (chunk == bytearray([int('0x01', 16)]) and countzeros == 3):
                    countzeros = 0
                    isNAL = False
                    isHeader = True
                elif chunk == bytearray([int('0x00', 16)]):
                    countzeros = countzeros + 1
                else:
                    countzeros = 0

                # change State
                if (isNAL and not isHeader):
                    if (initial_state == MarkovChain.ChannelState.GOOD):
                        noise_stream.write(chunk)
                    initial_state = ChannelSim.next_state(initial_state)
                elif (isHeader):
                    noise_stream.write(chunk)
        print(countNAL)
def worker(obj, QP):
    obj.runHEVCEncoderNoVerbose(QP)
def decode(obj):
    obj.decodeHEVC()


def checkCompletedFile():
    origWD = os.getcwd()
    os.chdir(resultPath+"str_D1")
    regex = re.compile(r'\d+')
    listdoneD1=[]
    listdoneD2=[]
    for file in glob.glob("*.hevc"):
        listdoneD1.append(regex.findall(file))
    os.chdir(origWD)
    os.chdir(resultPath+"str_D2")
    for file in glob.glob("*.hevc"):
        listdoneD2.append(regex.findall(file))
    os.chdir(origWD)
    return listdoneD1,listdoneD2




if not os.path.exists(resultPath+'str_D1_noise_p_%.3f/'%(p)):
    os.makedirs(resultPath+'str_D1_noise_p_%.3f/'%(p))
if not os.path.exists(resultPath+'str_D2_noise_p_%.3f/'%(p)):
    os.makedirs(resultPath+'str_D2_noise_p_%.3f/'%(p))
if not os.path.exists(resultPath+'str_org_noise_p_%.3f/'%(p)):
    os.makedirs(resultPath+'str_org_noise_p_%.3f/'%(p))
for i in range (QPM_min,QPM_max,QPMstep):
    for j in range (QP_min,i,QPstep):
        listBitStreamD1FileName.append([resultPath+"str_D1/str_D1_%d_%d.hevc"%(j,i),resultPath+"str_D1_noise_p_%.3f/str_D1_%d_%d.hevc"%(p,j,i)])
        listBitStreamD2FileName.append([resultPath+"str_D2/str_D2_%d_%d.hevc"%(j,i),resultPath+"str_D2_noise_p_%.3f/str_D2_%d_%d.hevc"%(p,j,i)])

countprogress = 0
nallistlost1=[]
nallistlost2=[]

for i in listBitStreamD1FileName:
    addNoiseToSignalNAL3(i[0],i[1],MarkovChain.ChannelState.GOOD,p,r,iteration)
    countprogress = countprogress + 1 
    print ("Simulation MDC Channel 1: %d/%d"%(countprogress,len(listBitStreamD1FileName)))
countprogress = 0

for j in listBitStreamD2FileName:
    addNoiseToSignalNAL3(j[0],j[1],MarkovChain.ChannelState.GOOD,p,r,iteration)
    countprogress = countprogress + 1 
    print ("Simulation MDC Channel 2: %d/%d"%(countprogress,len(listBitStreamD2FileName)))

            
for i in range(QP_min,QPM_max,QPstep):
    listBitStreamOrgFileName.append([resultPath+"str_org/str_org_%d.hevc"%(i),resultPath+"str_org_noise_p_%.3f/str_org_%d.hevc"%(p,i)])

countprogress = 0
for i in listBitStreamOrgFileName:
    addNoiseToSignalNAL3(i[0],i[1],MarkovChain.ChannelState.GOOD,p,r,iteration)
    countprogress = countprogress + 1 
    print ("Simulation SDC Channel SDC: %d/%d"%(countprogress,len(listBitStreamOrgFileName)))

# # Decode Noisy sequences
# for i,j,k in zip(listDecoderMdc,listPOCD1Noise,listPOCD2Noise):
#     P01_mean, P11_mean, P21_mean, MDC1PSNR_list = i.merge2Frame8x8withlostFrame(300,QPPath+j,QPPath+k)
# #get size
# for i,j in zip(listBitStreamD1FileName,listBitStreamD2FileName):
#     os.path.getsize(outputFilePath+i)
#     os.path.getsize(outputFilePath+j)
#     bitrate1 = (sizeD1 * 8 / 300) * 30 / 1000
#     bitrate2 = (sizeD2 * 8 / 300) * 30 / 1000
# result.append([P01_mean, P11_mean, P21_mean, sizeD1, sizeD2, PSDC_mean, sizeSDC])
# plt.plot(SDCPSNR_list, label="SDC(%d) %.3f" % (QP, PSDC_mean))
# plt.plot(MDC1PSNR_list, label="MDC(%d,%d) %.3f" % (QP, QPM, P01_mean))
# plt.plot(MDC2PSNR_list, label="MDC(%d,%d) %.3f" % (QP, QP, P02_mean))
# plt.xlabel("Frame No")
# plt.ylabel("PSNR [dB]")
# plt.legend()
# plt.title("Comparison of the same rate MDC and SDC")
# plt.show()
# with open("NoisePerf.csv", "w") as file:
#     writer = csv.writer(file)
#     writer.writerow(["P0,P1,P2,R1,R2,PSDC,RSDC"])
#     writer.writerows(result)
