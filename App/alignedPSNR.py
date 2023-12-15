# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from skimage.metrics import peak_signal_noise_ratio
import numpy as np
import sys
import pdb
import matplotlib.pyplot as plt
import pandas as pd
def find_best_match(iDecoded,delta,seq,ref_seq, range_limit):
    """
    Finds the frame in seq that best matches ref_frame within a given range.
    :param ref_frame: The reference frame
    :param seq: The sequence to search for the best match
    :param range_limit: The number of frames before or after the current position to search for the best match
    :return: The index of the best matching frame in seq
    """
    best_match_idx = None
    min_mse = float("inf")
    for i in range(max (iDecoded+delta-range_limit,0) , min(iDecoded+delta+range_limit, min(len(ref_seq),len(seq))-1)):
        try:
            mse = np.mean((seq[iDecoded] - ref_seq[i]) ** 2)
        except IndexError:
            pdb.set_trace()
        if mse < min_mse:
            min_mse = mse
            best_match_idx = i
    return best_match_idx
def compare_frames(seq,ref_seq,limit):
    psnr_list = []
    delta = 0
    for i in range(limit):
        best_match_idx = find_best_match(i,delta,seq,ref_seq, range_limit=300)
        if best_match_idx is not None:
            diff = peak_signal_noise_ratio(seq[i],ref_seq[best_match_idx])
            psnr_list.append(diff)
            if (best_match_idx!=i+delta):
                print ("Offset frame %d and %d" %(i,best_match_idx))
                # delta += best_match_idx-(i+delta)
                # print ("Delta Frame is {}".format(delta))
        elif (i+delta>=len(ref_seq) and i < len(seq)):
            diff = peak_signal_noise_ratio(seq[i],ref_seq[-1])
            psnr_list.append(diff)
        else:
            diff = peak_signal_noise_ratio(seq[-1],ref_seq[-1])
            psnr_list.append(diff)
    return psnr_list
def read_yuv420(file_path, width, height):
    """
    Reads a YUV420 file and returns a 3D numpy array
    :param file_path: The path to the YUV420 file
    :param width: The width of the video
    :param height: The height of the video
    :return: A 3D numpy array containing the video frames
    """
    with open(file_path, 'rb') as f:
        frames = []
        while True:
            Y = np.fromfile(f, np.uint8, width * height)
            if not Y.size:
                break
            U = np.fromfile(f, np.uint8, (width * height) // 4)
            V = np.fromfile(f, np.uint8, (width * height) // 4)
            frames.append(Y)
    return np.array(frames)
if __name__ == "__main__":
    # parse arguments
    if len(sys.argv) != 5:
        print("Usage: python3 %s <width> <height> <input_file> <ref_file>" % sys.argv[0])
        exit(1)
    w = int(sys.argv[1])
    h = int(sys.argv[2])
    inputFile = sys.argv[3]
    refFile = sys.argv[4]
    frame_refs = read_yuv420(refFile, w, h)
    frame_decs_noise = read_yuv420(inputFile, w, h)
    psnr_frame_noise = compare_frames(frame_refs,frame_decs_noise,len(frame_refs)-1)
    psnr_frame_noise = [value for value in psnr_frame_noise if value > 15]
    print ("PSNR Mean is {}".format(np.mean(psnr_frame_noise)))
    print ("PSNR STD is {}".format(np.std(psnr_frame_noise)))
    # Export psnr_frame_noise to csv file, but with the first row as the header
    df = pd.DataFrame({"frame_num": np.arange(len(psnr_frame_noise)), "psnr": psnr_frame_noise})
    df.to_csv("MDC.csv", index=False)
    plt.plot(psnr_frame_noise)
    plt.show()
