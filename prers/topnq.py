__author__ = 'franchoco'
from core import utils
from prer import PreR

class TopNQ(PreR):
    def __init__(self, f, n):
        PreR.__init__(self, f)
        self.names = {}
        self.n = n

    def __call__(self, d):
        qname = d['queries'][0]['qname'].lower()
        flags =  int(d['flags'], 16)
        is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        #print str(flags)
        if not is_answer:
            if self.names.has_key(qname):
                self.names[qname] += 1
            else:
                self.names[qname] = 1

    def get_data(self):
        last_n = dict(utils.keyswithmaxvals(self.names, self.n))
        return last_n

    def reset(self):
        self.names.clear()