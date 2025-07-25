import timer
import time

def main(): 
    t = timer.Timer()
    t.start_time()
    time.sleep(10) # 10 seconds
    t.end_time()
    t.getTotalTime()


if __name__ == '__main__':
    main()
