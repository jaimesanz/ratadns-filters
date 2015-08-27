__author__ = 'franchoco'

import time

class PacketsQueriesAndAnswersPerSecond(object):
    def __init__(self, f):
        self.pcounter = 0
        self.qcounter = 0
        self.acounter = 0
        self.start = time.time()
        self.f = f

    def __call__(self, d):
        flags =  int(d['flags'], 16)
        is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        self.pcounter += 1
        if is_answer:
            self.acounter += 1
        else:
            self.qcounter += 1

    def get_data(self):
        data = {}
        t=time.time()
        data['pps'] = self.pcounter / (t - self.start)
        data['qps'] = self.qcounter / (t - self.start)
        data['aps'] = self.acounter / (t - self.start)
        return data

    def get_file(self):
        return self.f

    def reset(self):
        self.pcounter = self.qcounter = self.acounter = 0
        self.start = time.time()