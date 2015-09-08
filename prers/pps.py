__author__ = 'franchoco'
from prer import PreR
import time

class PacketsPerSecond(PreR):
    def __init__(self, f):
        PreR.__init__(self, f)
        self.counter = 0
        self.start = time.time()

    def __call__(self, d):
        self.counter += 1

    def get_data(self):
        data = { 'pps' : self.counter / (time.time() - self.start) }
        return data

    def reset(self):
        self.counter = 0
        self.start = time.time()