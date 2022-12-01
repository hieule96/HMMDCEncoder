#!/bin/bash


rm QP1.mp4
rm QP2.mp4

MP4Box -hint -fps 30 -add QP1.hevc QP1.mp4
MP4Box -hint -fps 30 -add QP2.hevc QP2.mp4

../evalTools/RTP_transmitVideo -f -n QP1.mp4 -m 1 -r traceQP1.txt
../evalTools/RTP_transmitVideo -f -n QP2.mp4 -m 1 -r traceQP2.txt
python PLR-Simulator.py traceQP1.txt 5
python PLR-Simulator.py traceQP2.txt 5
../evalTools/etmp4 -i QP1.mp4 -o QP1_n -t TX_traceQP1.txt -r RX_traceQP1.txt -s 52000
../evalTools/etmp4 -i QP2.mp4 -o QP2_n -t TX_traceQP2.txt -r RX_traceQP2.txt -s 52000

../Lib/dec265 -c -o QP1_n.yuv -a ErrorDecodingFile1.txt QP1_n.hevc
../Lib/dec265 -c -o QP2_n.yuv -a ErrorDecodingFile2.txt QP2_n.hevc