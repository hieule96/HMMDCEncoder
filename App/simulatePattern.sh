#!/bin/bash

#cp ../../HMMDCEncoder/SrcVideo/BQMall_Full/QP1_BQMall_5_1.hevc QP1.hevc
#cp ../../HMMDCEncoder/SrcVideo/BQMall_Full/QP2_BQMall_5_1.hevc QP2.hevc
#cp ../../HMMDCEncoder/SrcVideo/BQMall_Full/QP1_BQMall_5_1_dec.csv QP1_dec.csv
#cp ../../HMMDCEncoder/SrcVideo/BQMall_Full/QP2_BQMall_5_1_dec.csv QP2_dec.csv

#MP4Box -hint -fps 60 -mtu 1500 -add QP1.hevc QP1.mp4
#MP4Box -hint -fps 60 -mtu 1500 -add QP2.hevc QP2.mp4
#../evalTools/RTP_transmitVideo -f -n QP1.mp4 -m 1 -r traceQP1.txt
#../evalTools/RTP_transmitVideo -f -n QP2.mp4 -m 1 -r traceQP2.txt
python PLR-SimulatorPattern_ns3.py traceQP1.txt packet_status_output_channel1.txt 0
python PLR-SimulatorPattern_ns3.py traceQP2.txt packet_status_output_channel2.txt 0
../evalTools/etmp4_0xFF -i QP1.mp4 -o QP1_n -t TX_traceQP1.txt -r RX_traceQP1.txt -s 52000
../evalTools/etmp4_0xFF -i QP2.mp4 -o QP2_n -t TX_traceQP2.txt -r RX_traceQP2.txt -s 52000
mv QP1_n.hevc ../../HMMDCEncoder/QP1_n.hevc
mv QP2_n.hevc ../../HMMDCEncoder/QP2_n.hevc
mv QP1_dec.csv ../../HMMDCEncoder/
mv QP2_dec.csv ../../HMMDCEncoder/
