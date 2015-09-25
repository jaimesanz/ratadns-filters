__author__ = 'sking32'
from prer import PreR
class NullPreR(PreR):
    def __init__(self, f):
        PreR.__init__(self,f)
    def __call__(self, d):
        pass
    def get_data(self):
        return None
    def reset(self):
        pass
