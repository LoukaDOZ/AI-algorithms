import math
import time
import sys

class Clock():
    def __init__(self):
        self._start = 0
    
    def start(self):
        self._start = time.time()
    
    def get_diff(self):
        return time.time() - self._start
    
    def get_time(self):
        time_diff = self.get_diff()
        ms = math.floor(time_diff * 1000) % 1000
        s = math.floor(time_diff) % 60
        m = math.floor(time_diff / 60)
        return m, s, ms
    
    def get_str_time(self):
        m, s, ms = self.get_time()
        return "{:02d}:{:02d}.{:03d}".format(m, s, ms)

def progress_bar(count, total, clock, title):
    bar_len = 10
    ratio = count / total
    percent = round(100 * ratio, 1)

    filled_len = math.floor(bar_len * ratio)
    empty_len = bar_len - filled_len

    sys.stdout.write("\r[{}{}] {}% ({}/{}) {} - {}".format('#' * filled_len, '-' * empty_len, percent, count, total, clock.get_str_time(), title))
    sys.stdout.flush()

    if ratio == 1:
        print()