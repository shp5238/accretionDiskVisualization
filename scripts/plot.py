#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""plot.py 
This file contains the code for data compression from 
a 2d array to a 2d array such as averaging data wrt 
to an axis as well as graphing data for relevant 
dissipation plots. 
"""

# IMPORTS

# Python Modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors 
import math

# Other
import os
import athena_read

# ---- ---- Data Scaling Methods  ---- ---- #
"""
Computes the integral of a quantity manually using loops.
Used for <divergence> wrt phi. rarely used.
"""
def scale_wrt_phi(input_arr, theta): #of format [phi, theta]
    # Input array validation
    if input_arr.shape != (256, 256):
        raise ValueError(f"Input array is not of the correct shape: {input_arr.shape}")

    # theta array validation
    if theta.shape != (256,):
        raise ValueError(f"Theta array is not of the correct shape: {theta.shape}")    

    # Integration of theta for each phi
    yArray = np.zeros(len(input_arr))

    for i in range(len(input_arr)):
      theta_sum = 0.0
      for j in range(len(input_arr[0]) - 1):
        d_theta = theta[j+1] - theta[j]
        theta_sum += (1/2) * input_arr[i][j] * np.sin(theta[j]) * d_theta #left Riemann sum
        #accurate if data is decreasing
      yArray[i] = theta_sum
      #print(yArray[i])
    return yArray


"""
Computes the integral of a quantity manually using loops.
Used for <divergence> Wrt phi.
Parameters: input_arr.shape = [phi, theta]
  int[int []], 2d array
Returns: yArray: int[] of format [theta]
"""
def scale_wrt_theta(input_arr, phi): #of format [phi, theta]
    # Input array validation
    if input_arr.shape != (256, 256):
        raise ValueError(f"Input array is not of the correct shape: {input_arr.shape}")
    
    # phi array validation
    if phi.shape != (256,): 
        raise ValueError(f"Phi array is not of the correct shape: {phi.shape}")

    # Integration of phi for each theta
    yArray = np.zeros(len(input_arr[0]))

    for i in range(len(input_arr[0])):
      phi_sum = 0.0
      for j in range(len(input_arr)-1):
        d_phi = phi[j+1] - phi[j]
        phi_sum += (1/(2* math.pi)) * input_arr[j][i] * d_phi
      yArray[i] = phi_sum
      #print(yArray[i])
    return yArray


# ---- ---- Plotting Method ---- ---- #
"""
This function takes in a given x and y axis and plots the data.
Argument(s): xArr: 1d [float], yArr: 1d[float]
Optional:  xlabel="Theta / pi", ylabel="Dissipation Profile", rad=-1 (sentinel by default)
Returns: None
"""
def plot_data(xArr, yArr, xlabel="Theta / pi", ylabel="Dissipation Profile", rad=-1):
    plt.plot(xArr, yArr)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f"Dissipation profile wrt theta generated at radius: {rad}")
    plt.show()
    return None



# ---- ---- Data Extraction Methods ---- ---- #

"""
Extracts 'theta' data from an .athdf output file and saves it as a NumPy binary file
for convenient use in graph plotting and further analysis. 

Argument(s): file_path (str): full path to the .athdf file
Returns: None
"""
def save_theta(file_path):
    data = athena_read.athdf(file_path) # reads file
    theta = data['x2v']
    path = os.path.join(os.getcwd(), "theta.npy")
    np.save(path, theta)
    return None

"""
Extracts 'phi' data from an .athdf output file and saves it as a NumPy binary file     
for convenient use in graph plotting and further analysis.

Argument(s): file_path (str): full path to the .athdf file
Returns: None
"""
def save_phi(file_path):
    data = athena_read.athdf(file_path) # reads file
    phi = data['x3v']   
    path = os.path.join(os.getcwd(), "phi.npy")
    np.save(path, phi)
    return None
