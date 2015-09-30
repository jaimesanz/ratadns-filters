__author__ = 'franchoco'
from core.utils import keyswithmaxvals
from prer import PreR

class TopN(PreR):
    def __init__(self, f):
        PreR.__init__(self, f)
        self.names = {}
        self.n = 10

    def __call__(self, d):
        qname = d['queries'][0]['qname'].lower()

        if self.names.has_key(qname):
            self.names[qname] += 1
        else:
            self.names[qname] = 1

    def get_data(self):
        last_n = dict(keyswithmaxvals(self.names, self.n))
        return last_n

    def reset(self):
        self.names.clear()
