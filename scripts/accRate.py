#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" accRate.py
Plots the accretion rate at a given radial index value by time. 
"""

# IMPORTS
import sys
import os

# Helper Module
import athena_read

# Other Python Modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

"""
Outputs the accretion rate at a given radial index value for a single file. 
Arguments: 
String: file_path, int r_i (radial index)
Returns: None
"""
def run_program(file_path, r_i, output_f=""):
    # TODO: rewrite debugging code as error validation to catch errors. error handling
   
    """ 
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



    """
    if not os.path.isfile(file_path):
        print(f"Error: File not found in worker: {file_path}", file = sys.stderr)
        print(f"Error: CWD in worker {os.getcwd()}", file = sys.stderr)
        print(f"Volume mounted:  {os.path.ismount('/Volumes/Athena')}", file = sys.stderr)
        print(f"Listing dir: {os.listdir('/Volumes/Athena/summer25files')}", file = sys.stderr)
        sys.exit(1)
    """
    
    # Read the file and validate data
    data = athena_read.athdf(file_path)
    key_validation(data)

    # Get spherical coordinates
    r = data['x1v']
    theta = data['x2v']
    phi = data['x3v']

    # Get rho values for the given r_i
    rho = data['rho']
    v_r = data['vel1']

    # Create d_phi for integral
    d_phi = phi[1] - phi[0]

    # Initialize array for our sum over theta and transpose our var array
    theta_sum = np.zeros((len(phi)))
    t_rho = np.transpose(rho, (1,0,2))
    t_v_r = np.transpose(v_r, (1,0,2))

    rho_r = t_rho[:,:,r_i]
    v_r_r = t_v_r[:,:,r_i]


    # For loop to sum across theta (0 to pi), need to multiply each element by sin(theta) and d_theta
    # Note that d_theta is not constant, this causes our new array length to be 1 less than the original
    for i in range(1,len(theta)):
        d_theta = theta[i]-theta[i-1]

        theta_sum += rho_r[i] * v_r_r[i] * np.sin(theta[i]) * d_theta

    # Initialize array for our sum over phi
    phi_sum = 0

    # For loop to sum across phi (0 to 2pi)
    for j in range(len(phi)):
        phi_sum += theta_sum[j] * d_phi

    # Initialize variable for accretion rate
    acc_rate = 0

    # Get accretion rate by multiplying by r^2
    acc_rate = phi_sum * r[r_i]**2

    print(f"Processed {file_path} with radial index {r_i}, PID: {os.getpid()}") 

    # Save array to .npy file
    if output_f != "":
        np.save(output_f, acc_rate)

    
    print(acc_rate)
       
    return acc_rate
       

"""
Checks for rho, v_r, r, theta, and phi keys
"""
def key_validation(data):
    if not "rho" in data.keys():
        raise ValueError("rho is not a key, choose another athdf file") 
    if not "vel1" in data.keys():
        raise ValueError("v_r is not a key, choose another athdf file")
    if not "x1v" in data.keys():
        raise ValueError("x1v (r) is not a key, choose another athdf file")
    if not "x2v" in data.keys():
        raise ValueError("x2v (theta) is not a key, choose another athdf file")    
    if not "x3v" in data.keys():
        raise ValueError("x3v (phi) is not a key, choose another athdf file")   


def main():
    args = sys.argv[1:]
    if len(args) < 2: 
        print("Usage: python accRate.py <radius> <file> <optional output_path>", file=sys.stderr)
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
