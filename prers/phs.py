__author__ = 'franchoco'

class PacketHasUnderscore(object):
    def __init__(self, f):
        self.f = f
        self.names = {}

    def __call__(self, d):
        flags =  int(d['flags'], 16)
        is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        if not is_answer:
            query = d['queries'][0]
            qname = query['qname']
            qtype = int(query['qtype'], 16)
            sender = d['source']
            if "_" in qname and qtype in [1, 2, 6, 15]:
                if self.names.has_key(sender):
                    self.names[sender]['cnt'] += 1
                    self.names[sender]['queries'].append(query)
                else:
                    self.names[sender] = { 'cnt' : 1 , 'queries' : [query] }

    def get_data(self):
        return self.names

    def get_file(self):
        return self.f

    def reset(self):
        self.names.clear()
