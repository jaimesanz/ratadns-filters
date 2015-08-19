__author__ = 'franchoco'

import time

class PacketsPerSecond(object):
    def __init__(self, f):
        self.counter = 0
        self.start = time.time()
        self.f = f

    def __call__(self, d):
        self.counter += 1

    def get_data(self):
        data = { 'pps' : self.counter / (time.time() - self.start) }
        return data

    def get_file(self):
        return self.f

    def reset(self):
        self.counter = 0
        self.start = time.time()