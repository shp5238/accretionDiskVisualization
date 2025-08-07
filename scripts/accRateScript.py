#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""accRateScript.py 
This program acts as a controller to parse command line arguments, 
share global parameters with all worker processes, find all files 
to be processed, and runs CPU-bound multi-processing to quickly and 
efficiently display the results of the time averaged accretion rate code.

Folder Format: 
code/
|__ script.py           # Script parser for time averaged accretion rate
|__ program.py          # Time-averaged dissipation profile code
|__ athena_read.py      # shorter athena_read file for easy processing. 
|__ plot.py             # Plotting and data reduction code for one axis
|__ *.athdf             # All .athdf files must be located here
|__ output/             # Output directory for graphs and results

Usage: python(3) script.py <one_arg> <two_arg>
"""

# IMPORTS

# System, OS, and CLI utilities
import os # OS interaction
import sys # sys functions
import argparse # CLI parsing
import subprocess # run external commands

# Multiprocessing libraries: 
from concurrent.futures import ProcessPoolExecutor
from functools import partial

# Custom Helper Modules
import worker
import plot
import timer

# Other Python modules
import numpy as np
import re

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


def sort_files(file_list):
    def extract_num(file):
        match = re.search(r'\.(\d+)\.athdf$', file)
        return int(match.group(1)) if match else -1

    file_list.sort(key=lambda f: extract_num(os.path.basename(f)))   # returns None
    return file_list

"""
This function recursively walks upward from the file location to find the project root. 
marker_name can be a directory like ".git" or a file (".yml")
"""
def find_proj_root(marker_name):
    try: # Start from the script's direction
        curr = os.path.abspath(os.path.dirname(__file__))
    except NameError: 
        curr = os.getcwd()

    while True: 
        # looks for file or directory
        if os.path.isdir(os.path.join(curr, marker_name)) or os.path.isfile(os.path.join(curr, marker_name)):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr: # Reached filesystem root 
            print(parent)
            raise FileNotFoundError(f"Could not fiind marker: {marker_name}.")
        curr = parent    

# ==== ==== END OF Validation Helper Functions ==== ==== #


# ==== ==== Core Worker ===== ===== #
def run_worker_script(file_path, radius):
    # Use absolute paths so worker processes can find external hard drives
    file_path = os.path.abspath(file_path) # path of athdf file
    
    # Create output filename based on input filename
    output_file = file_path + ".npy"

    project_root = find_proj_root('.git')
    # Debugging: print(f"Root: {project_root}")
    worker_path = os.path.join(project_root, 'scripts', 'accRate.py')

    result = subprocess.run(
        [sys.executable, worker_path, str(radius), file_path, output_file],
        capture_output=True, text=True
    )
    
    # Check if worker.py succeeded
    if result.returncode != 0: 
        print(f"Error: worker.py failed on {file_path}:\n{result.stderr}") 
        return None

    # Load the .npy result
    try: 
        arr = np.load(output_file)
    except Exception as e: 
        print(f"Error: failed to load {output_file}: {e}")
        return None   

    # Delete the .npy file when no longer needed 
    os.remove(output_file)

    return arr 


# ==== ==== THE MAIN FUNCTION ==== ==== #
def main():
    # Positional Arguments
    parser = argparse.ArgumentParser(description="Usage: python(3) script.py <radius>")
    parser.add_argument("radius", type=radial_int, help="Integer radius index between -512 and 511.")
    
    # Optional Arguments    
    parser.add_argument("-t", "--time", 
    action="store_true",
    dest="time_measured",
    help="Option to measure and display time of program.")
    
    parser.add_argument("-d", "--dir", default=".", help='Path to the drectory contianing the .athdf files (default: current directory)')    

    args = parser.parse_args()
    
    # Can manually specify files here
    # file_list = ["disk.out1.00018.athdf", "disk.out1.00019.athdf"]
    
    """
    # TODO: add --start, -s and --end, -e and --inc, -i flags
    os.path.exists(filename)

    specify range for customization
    - assumes filenames follow strict pattern
    - selective filtering of athdf files
    """

    # ---- ---- Find the files to process ---- ---- #
    data_dir = os.path.abspath(args.dir) # Normalizing the path
    file_list = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".athdf")]

    if not file_list: # file list is empty
        print(f"There are no .athdf files detected in directory: {args.dir}")
        return # Should stop the program, since nohing to compute

    file_list = sort_files(file_list)

    # Debugging which files used.
    print(f"Files used: {file_list}") 
    first_f = file_list[0] # fastest
    print(first_f)

    if args.time_measured:
        t = timer.Timer()
        t.start_time()

    worker_fn = partial(run_worker_script, radius=args.radius)

    # If doesn't exist, save theta and phi arrays for later
    theta_path = os.path.abspath("theta.npy")
    phi_path = os.path.abspath("phi.npy")
    
    if (not os.path.exists(theta_path)):
        plot.save_theta(first_f)
    if (not os.path.exists(phi_path)):
        plot.save_phi(first_f)

    # Create output filename based on input filename
    output_file = file_list[0][0:-7] + ".npy"

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(worker_fn, file_list))
    
    """ Change this debug to work on 1d results array    
    # TODO: don't keep this debug, but write a check to ensure correct type
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
    """
    
    
    loading = "./theta.npy"
    try: 
        theta = np.load(loading)
        loading = "./phi.npy"
        phi = np.load(loading)
    except Exception as e: 
        print(f"Error: failed to load {loading}: {e}")
        return None 
    
    
    # Scale the yaxis data
    yArr = results
    print(yArr)  
  
    # Define x array
    xArr = list(range(len(results)))


    if args.time_measured:
        t.end_time()

    plot.plot_data(xArr, yArr, rad=args.radius, xlabel=f"Time: 0 to {len(results)-1} seconds", ylabel="Accretion rate at r", title="Accretion Rate as a function of time")	

    print("Program executed successfully!")
    if args.time_measured:
        t.getTotalTime()

	
if __name__ == "__main__":
	main()
		
# End of program

