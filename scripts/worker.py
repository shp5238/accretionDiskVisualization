#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" worker.py

"""

# IMPORTS
import sys
import os

import athena_read
import numpy as np


"""
Arguments: 
String: file_path, int radius
Returns: None
"""
def run_program(file_path, radius, output_f=""):
    # Debugging file access issues
    print(f"[INFO] Attempting to open: {file_path}", file=sys.stderr)
    print(f"[INFO] Absolute path: {os.path.abspath(file_path)}", file=sys.stderr)

    if not os.path.exists(file_path):
       print(f"[ERROR] File does NOT exist at: {file_path}", file=sys.stderr)
       print(f"[DEBUG] Current Working Dir: {os.getcwd()}", file=sys.stderr)
       print(f"[DEBUG] Volume Mounted? /Volumes/Athena → {os.path.ismount('/Volumes/Athena')}", file=sys.stderr)
       parent_dir = os.path.dirname(file_path)
       print(f"[DEBUG] Files in {parent_dir}:", os.listdir(parent_dir), file=sys.stderr)
       sys.exit(1)    





    """
    if not os.path.isfile(file_path):
        print(f"Error: File not found in worker: {file_path}", file = sys.stderr)
        print(f"Error: CWD in worker {os.getcwd()}", file = sys.stderr)
        print(f"Volume mounted:  {os.path.ismount('/Volumes/Athena')}", file = sys.stderr)
        print(f"Listing dir: {os.listdir('/Volumes/Athena/summer25files')}", file = sys.stderr)
        sys.exit(1)
    """
    
    f = os.path.basename(file_path) # get filename
    data = athena_read.athdf(f) # reads file
    key_validation(data)

    # Get relevant quantities
    Fr1 = data['Fr1']
    Fr2 = data['Fr2']
    Fr3 = data['Fr3']

    # Get spherical coordinates
    r = data['x1v']
    theta = data['x2v']
    phi = data['x3v']

    # Initializing reusable constants
    len_r = len(r)
    len_th = len(theta)
    len_phi = len(phi)

    # Initialze arrays
    d_r = np.zeros_like(r)
    d_theta = np.zeros_like(theta)
    d_phi = np.zeros_like(phi)
    sin_theta = np.zeros_like(theta) #similar dimensions, only different values.

    # Appropriately adjust these arrays
    d_r[1:-1] = (r[2:] - r[:-2]) / 2
    d_theta[1:-1] = (theta[2:] - theta[:-2]) / 2
    d_phi[1:-1] = (phi[2:] - phi[:-2]) / 2
    sin_theta[:] = np.sin(theta[:])

    # Initialize arrays
    Div = np.zeros_like(Fr1) # total divergence
    t1 = np.zeros_like(Div) #r term
    t2 = np.zeros_like(Div) # theta term
    t3 = np.zeros_like(Div) # phi term

    # ---- Compute Divergence: ---- #
    # r term
    for i in range(1, len_r-1):
        a = Fr1[:, :, i+1] * (r[i+1] ** 2) * sin_theta[:]  # shape (256, 256)
        b = Fr1[:, :, i]   * (r[i]   ** 2) * sin_theta[:]
        t1[:, :, i] = (a - b) * d_theta[:] * d_phi[:]

    # theta term
    for j in range(1, len_th - 1):
        a = Fr2[:, j+1, :] * r[:] * sin_theta[j+1]  # shape (256, 512)
        b = Fr2[:, j, :]   * r[:] * sin_theta[j]
        t2[:, j, :] = (a - b) * d_phi[:, np.newaxis] * d_r

    # phi term
    for k in range(1, len_phi - 1):
        a = Fr3[k+1, :, :] * r[:]  # shape (256, 256)
        b = Fr3[k, :, :]   * r[:]
        t3[k, :, :] = (a - b) * d_theta[:, np.newaxis] * d_r

    # Total Divergence
    Div = t1 + t2 + t3

    # Compute Delta Volume
    d_Volume = (r[np.newaxis, np.newaxis, :] **2 ) * sin_theta[np.newaxis, :, np.newaxis] * d_r[np.newaxis, np.newaxis, :] * d_theta[np.newaxis, :, np.newaxis] * d_phi [:, np.newaxis, np.newaxis]

    result = np.where(d_Volume != 0, Div / d_Volume, 0)

    result = result[:, :, radius] #split so that there's less to store later.
    print(f"Processed {file_path} with radius {radius}, PID: {os.getpid()}") 

    # Save array to .npy file
    if output_f != "":
        np.save(output_f, result)
       
    return result
       


def key_validation(data):
    if not "Fr1" in data.keys():
        raise ValueError("Fr1 is not a key, choose another athdf file") 
    if not "Fr2" in data.keys():
        raise ValueError("Fr2 is not a key, choose another athdf file")
    if not "Fr3" in data.keys():
        raise ValueError("Fr3 is not a key, choose another athdf file")
    if not "x1v" in data.keys():
        raise ValueError("x1v (r) is not a key, choose another athdf file")
    if not "x2v" in data.keys():
        raise ValueError("x2v (theta) is not a key, choose another athdf file")    
    if not "x3v" in data.keys():
        raise ValueError("x3v (phi) is not a key, choose another athdf file")   

    """ For programmer use only, when running worker.py individually, uncomment
    assert ("Fr1" in data.keys()), "Fr1 is not a key, choose another athdf file"
    assert ("Fr2" in data.keys()), "Fr2 is not a key, choose another athdf file"
    assert ("Fr3" in data.keys()), "Fr3 is not a key, choose another athdf file"
    assert ("x1v" in data.keys()), "x1v (r) is not a key, choose another athdf file"
    assert ("x2v" in data.keys()), "x2v (theta) is not a key, choose another athdf file"
    assert ("x3v" in data.keys()), "x3v (phi) is not a key, choose another athdf file"
    """

def main():
    args = sys.argv[1:]
    if len(args) < 2: 
        print("Usage: python worker.py <radius> <file> <optional output_path>", file=sys.stderr)
        sys.exit(1)
    radius = int(args[0])
    file_path = args[1]
    if len(args) > 2:
        output_path = sys.argv[3]
        run_program(file_path, radius, output_path)
    else: # No output specified, just do computation
        run_program(file_path, radius)

if __name__ == "__main__":
    main()
