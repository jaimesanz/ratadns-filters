__author__ = 'franchoco'

class NameCounter(object):
    def __init__(self, f):
        self.f = f
        self.names = {}

    def __call__(self, d):
        qname = d['queries'][0]['qname'].lower()
        if self.names.has_key(qname):
            self.names[qname] += 1
        else:
            self.names[qname] = 1

    def get_data(self):
        return self.names

    def get_file(self):
        return self.f

    def reset(self):
        self.names = {}

