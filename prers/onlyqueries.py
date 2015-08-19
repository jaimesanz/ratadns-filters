__author__ = 'franchoco'

class OnlyQueries(object):
    def __init__(self, f):
        self.f = f
        self.l = []
    def __call__(self, d):
        #flags = d['flags']
	flags =  int(d['flags'], 16)
        is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        #print str(flags)
	if not is_answer:
            self.l.append(d)
    def get_data(self):
        return self.l
    def get_file(self):
        return self.f
    def reset(self):
        self.l = []