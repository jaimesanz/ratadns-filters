__author__ = 'franchoco'
from prer import PreR
class NameCounter(PreR):
    def __init__(self, f):
        PreR.__init__(self, f)
        self.names = {}

    def __call__(self, d):
        qname = d['queries'][0]['qname'].lower()
        if self.names.has_key(qname):
            self.names[qname] += 1
        else:
            self.names[qname] = 1

    def get_data(self):
        return self.names

    def reset(self):
        self.names = {}

