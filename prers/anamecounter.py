__author__ = 'sking32'
from prer import PreR
class AnswersNameCounter(PreR):
    def __init__(self, f):
        PreR.__init__(self, f)
        self.names = {}

    def __call__(self, d):
        flags =  int(d['flags'], 16)
    	is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        if is_answer:
            qname = d['queries'][0]['qname'].lower()
            if self.names.has_key(qname):
                self.names[qname] += 1
            else:
                self.names[qname] = 1

    def get_data(self):
        return self.names

    def reset(self):
        self.names = {}

