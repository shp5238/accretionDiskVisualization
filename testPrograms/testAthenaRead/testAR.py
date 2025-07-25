# testAR.py
# This file will test if athena_read.py works

import athena_read
import timer
import oldAR

def main():
    # code here
    
    # combine measure time functionality

    t = timer.Timer()
    f = "disk.out1.00018.athdf"

    # start the timer
    t.start_time()

    data = oldAR.athdf(f)
    # data = athena_read.athdf(f) # Read the file
    # key_validation(data)

    # end the timer 
    t.end_time()
    print("The program successfully executed!")
    
    # output total time
    t.getTotalTime()

    """
    Results: based on this test, there is no significant improvement between 
    the shorter athena_read and the longer version. 
    """


def key_validation(data):
    assert ("Fr1" in data.keys()), "Fr1 is not a key, choose another athdf file"
    assert ("Fr2" in data.keys()), "Fr2 is not a key, choose another athdf file"
    assert ("Fr3" in data.keys()), "Fr3 is not a key, choose another athdf file"
    assert ("x1v" in data.keys()), "x1v (r) is not a key, choose another athdf file"
    assert ("x2v" in data.keys()), "x2v (theta) is not a key, choose another athdf file"
    assert ("x3v" in data.keys()), "x3v (phi) is not a key, choose another athdf file"


if __name__ == "__main__":
    main()
