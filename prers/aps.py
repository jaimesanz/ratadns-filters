__author__ = 'raticate'
from prer import PreR
import time

class AnswersPerSecond(PreR):
    def __init__(self, f):
        PreR.__init__(self,f)
        self.counter = 0
        self.start = time.time()

    def __call__(self, d):
        flags =  int(d['flags'], 16)
        is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        if is_answer:
            self.counter += 1

    def get_data(self):
        data = { 'aps' : self.counter / (time.time() - self.start) }
        return data

    def reset(self):
        self.counter = 0
        self.start = time.time()