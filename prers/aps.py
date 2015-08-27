__author__ = 'raticate'

import time

class AnswersPerSecond(object):
    def __init__(self, f):
        self.counter = 0
        self.start = time.time()
        self.f = f

    def __call__(self, d):
        flags =  int(d['flags'], 16)
        is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        if is_answer:
            self.counter += 1

    def get_data(self):
        data = { 'aps' : self.counter / (time.time() - self.start) }
        return data

    def get_file(self):
        return self.f

    def reset(self):
        self.counter = 0
        self.start = time.time()