# testAR.py
# This file will test if athena_read.py works

import athena_read
import timer
import numpy as np
import plot

def main():
    # Measure time functionality
    t = timer.Timer()
    f = "disk.out1.00018.athdf"

    # start the timer
    t.start_time()

    data = athena_read.athdf(f) # Read the file
    key_validation(data)

    theta = data['x2v']
    xArr = (theta/np.pi)
    yArr = np.linspace(0, 10, 256)  

    # end the timer 
    t.end_time()
    print("The program successfully executed!")

    # plot the data
    plot.plot_data(xArr, yArr)
        
    # output total time
    t.getTotalTime()


def key_validation(data):
    assert ("Fr1" in data.keys()), "Fr1 is not a key, choose another athdf file"
    assert ("Fr2" in data.keys()), "Fr2 is not a key, choose another athdf file"
    assert ("Fr3" in data.keys()), "Fr3 is not a key, choose another athdf file"
    assert ("x1v" in data.keys()), "x1v (r) is not a key, choose another athdf file"
    assert ("x2v" in data.keys()), "x2v (theta) is not a key, choose another athdf file"
    assert ("x3v" in data.keys()), "x3v (phi) is not a key, choose another athdf file"


if __name__ == "__main__":
    main()
