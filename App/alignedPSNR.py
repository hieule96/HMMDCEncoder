# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from skimage.metrics import peak_signal_noise_ratio
import numpy as np

def find_best_match(iDecoded,seq,ref_seq, range_limit=10):
    """
    Finds the frame in seq that best matches ref_frame within a given range.
    :param ref_frame: The reference frame
    :param seq: The sequence to search for the best match
    :param range_limit: The number of frames before or after the current position to search for the best match
    :return: The index of the best matching frame in seq
    """
    best_match_idx = None
    min_mse = float("inf")
    for i in range(max (iDecoded-10,0) , min(iDecoded+range_limit, min(len(ref_seq),len(seq)))):
        mse = np.mean((seq[iDecoded] - ref_seq[i]) ** 2)
        if mse < min_mse:
            min_mse = mse
            best_match_idx = i
    return best_match_idx
def compare_frames(seq,ref_seq,limit=501):
    psnr_list = []
    for i in range(min (len(seq),limit)):
        best_match_idx = find_best_match(i,seq,ref_seq, range_limit=10)
        if best_match_idx is not None:
            diff = peak_signal_noise_ratio(seq[i],ref_seq[best_match_idx])
            psnr_list.append(diff)
        if (best_match_idx!=i):
            print ("Offset frame %d and %d" %(i,best_match_idx))
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
w = 1920
h = 1080
if __name__ == "__main__":
    frame_refs = read_yuv420("../RawVideo/Kimono1_1920x1080_24.yuv", w, h)
    frame_decs_noise = read_yuv420("../debugoutputCentralA.yuv", w, h)
    psnr_frame_noise = compare_frames(frame_decs_noise,frame_refs)
    frame_decs = read_yuv420("../VideoRef/Kimono16/recCentral_Kimono_8_1.yuv", w, h)
    psnr_frame = compare_frames(frame_decs,frame_refs)

    print ("Org %.3f" %np.mean(psnr_frame))
    print ("Noise %.3f"%np.mean(psnr_frame_noise))