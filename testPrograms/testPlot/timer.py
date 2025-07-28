# timer.py 
import time

class Timer: 
    def __init__(self):
       self.start = 0.0
       self.end = 0.0

    def start_time(self):
        self.start = time.time()

    def end_time(self):
        self.end = time.time()

    def getTotalTime(self):
        self.sec_to_min((self.end - self.start))
        # alternate def
        # f"{end-start:.2f}" seconds

    """
    Takes in a integer value for the seconds and converts to 
    a user-readable string to display time. Largest unit is days. 
    Argument(s): float s
    Returns: None
    """
    def sec_to_min(self,s: float) -> None: 
        assert isinstance(s, float), "Seconds must be a float."
        assert s>=0, "Seconds must be non-negative."
        min, secs = divmod(s, 60)
        hours = 0
        if min > 60: 
            hours, min = divmod(min, 60)
        days = 0
        if hours > 24: 
            days, hours = divmod(hours, 24)
    
        parts = []
        if days: 
            parts.append(f"{int(days)} day{'s' if days!= 1 else ''}")
        if hours: 
            parts.append(f"{int(hours)} hour{'s' if hours!= 1 else ''}")
        if min: 
            parts.append(f"{int(min)} minute{'s' if min!= 1 else ''}")
        if secs: 
            parts.append(f"{int(secs)} second{'s' if secs!= 1 else ''}")


        if parts: 
            print("Total time is " + " and ".join(parts) + ".")
        else: 
            print("Total time is 0 seconds.")
    
        return None

