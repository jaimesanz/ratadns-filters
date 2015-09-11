__author__ = 'franchoco'
from prer import PreR
class Identity(PreR):
    def __init__(self, f):
        PreR.__init__(self,f)
        self.l = []
    def __call__(self, d):
        self.l.append(d)
    def get_data(self):
        return self.l
    def reset(self):
        self.l = []