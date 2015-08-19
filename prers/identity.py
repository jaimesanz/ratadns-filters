__author__ = 'franchoco'

class Identity(object):
    def __init__(self, f):
        self.f = f
        self.l = []
    def __call__(self, d):
        self.l.append(d)
    def get_data(self):
        return self.l
    def get_file(self):
        return self.f
    def reset(self):
        self.l = []