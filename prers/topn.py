__author__ = 'franchoco'
from .. import core
from core import utils

class TopN(object):
    def __init__(self, f, n):
        self.f = f
        self.names = {}
        self.n = n

    def __call__(self, d):
        qname = d['queries'][0]['qname'].lower()

        if self.names.has_key(qname):
            self.names[qname] += 1
        else:
            self.names[qname] = 1

    def get_data(self):
        last_n = dict(utils.keyswithmaxvals(self.names, self.n))
        return last_n

    def get_file(self):
        return self.f

    def reset(self):
        self.names.clear()