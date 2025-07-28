#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""script.py 
This program acts as a controller to parse command line arguments, 
share global parameters with all worker processes, find all files 
to be processed, and runs CPU-bound multi-processing to quickly and 
efficiently display the results of the time averaged dissipation code.

Folder Format: 
code/
|-- script.py           # Script parser for time averaged dissipation
|-- program.py          # Time-averaged dissipation profile code
|-- athena_read.py      # shorter athena_read file for easy processing. 
|-- plot.py             # Plotting and data reduction code for one axis
|-- *.athdf             # All .athdf files must be located here
|-- output/             # Output directory for graphs and results

Usage: python script.py <one_arg> <two_arg>
"""

# IMPORTS
import os
import argparse

# Multiprocessing libraries: 
from concurrent.futures import ProcessPoolExecutor
from functools import partial

import worker
import plot

import sys
import argparse
import subprocess

import numpy as np

# ==== ==== Validation Helper Functions ==== ==== #

def neg_to_pos_ind(neg_ind, length):
	if neg_ind < 0: 
		return length + neg_ind
	else: 
		printV1("Input index isn't negative.")

def radius_validation(rad, len_r, extra_info):
	if not (-len_r <= rad <= len_r -1):
	    raise ValueError(f"Radial index must be between -{len_r} and {max_len -1}. Out of bounds.")

	if extra_info and rad < 0: # if rad is neg and want additional info 
	    print("Are you sure you wanted to select a negative radius?")
	    print("This corresponds to index {neg_to_pos_ind(rad, len_r)}")
	return

def radial_int(value): 
    len_r = 512 
    try: 
        fvalue=int(value)
    except ValueError: #cant be converted into int
        raise argparse.ArgumentTypeError(f"{value} is not a valid int.")
    
    if not (-len_r <= fvalue <= len_r - 1): 
        raise ValueError(f"{fvalue} is out of bounds. Radius must be between -{len_r} and {len_r -1}.") 
    return fvalue


# ==== ==== END OF Validation Helper Functions ==== ==== #


# ==== ==== Core Worker ===== ===== #
def run_worker_script(file_path, radius):
    # Create output filename based on input filename
    output_file = file_path + ".npy"
    
    result = subprocess.run(
        [sys.executable, 'worker.py', str(radius), file_path, output_file],
        capture_output=True, text=True
    )
    
    # Check if worker.py succeeded
    if result.returncode != 0: 
        printf("Error: worker.py failed on {file_path:\n{result.stderr}}") 
        return None

    # Load the .npy result
    try: 
        arr = np.load(output_file)
    except Exception as e: 
        print(f"Error: failed to load {output_file}: {e}")
        return None   

    # Later: delete the .npy file when no longer needed 
    #os.remove(output_file)

    return arr 


# ==== ==== THE MAIN FUNCTION ==== ==== #
def main():
    parser = argparse.ArgumentParser(description="Usage: python(3) script.py <radius>")
    parser.add_argument("radius", type=radial_int, help="Integer radius index between -512 and 511.")
    args = parser.parse_args()
    
    file_list = ["disk.out1.00018.athdf", "disk.out1.00019.athdf"]
    
    worker_fn = partial(run_worker_script, radius=args.radius)

    # If doesn't exist, save theta and phi arrays for later
    theta_path = os.path.abspath("theta.npy")
    phi_path = os.path.abspath("phi.npy")
    if (not os.path.exists(theta_path)):
        plot.save_theta(file_list[0])
    if (not os.path.exists(phi_path)):
        plot.save_phi(file_list[0])

    # Create output filename based on input filename
    output_file = file_list[0][0:-7] + ".npy"

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(worker_fn, file_list))
        

    # Debugging: 
    for i, r in enumerate(results):
        if r is None:
            print(f"[DEBUG] results[{i}] is None")
        elif not isinstance(r, np.ndarray):
            print(f"[DEBUG] results[{i}] is NOT a NumPy array: {type(r)}")
        elif r.shape != (256, 256):
            print(f"[DEBUG] results[{i}] has shape {r.shape}")
        elif r.dtype == object:
            print(f"[DEBUG] results[{i}] has dtype=object")
    
    
    # Ensure arrays are 2d and numeric
    valid_arrs = [
        np.asarray(arr, dtype=np.float64)
        for arr in results
        if arr is not None and isinstance(arr, np.ndarray) and arr.shape == (256, 256)
    ]

    if not valid_arrs: # if empty 
        raise ValueError("No valid 256x256 arrays to average.")

    avg = np.zeros((256, 256), dtype=np.float64)
    for arr in valid_arrs:
        avg += arr

    avg /= len(valid_arrs)
    
    
    
    
    # TODO: add try and except for accessing these files
    theta = np.load("./theta.npy")
    phi = np.load("./phi.npy")
    
    # Scale the yaxis data from (256, 256) to (256)
    yArr = plot.scale_wrt_theta(avg, phi) # final y array

    # Define x array
    xArr = (theta / np.pi) 

    plot.plot_data(xArr, yArr, rad=args.radius)	

    print("Program executed successfully!")


	
if __name__ == "__main__":
	main()
		
# End of program

