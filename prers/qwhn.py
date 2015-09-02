__author__ = 'sking32'

#The result is a dict which keys are qnames
# with an underscore and the value is the list
# of dicts showing the sender, server and query
# for the queries with this qname
class QueriesWithUnderscoredName(object):
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
            server = d['dest']
            if "_" in qname and qtype in [1, 2, 6, 15]:
                if not self.names.has_key(qname):
                    self.names[qname] = []
                newQuery = {'sender': sender, 'server': server, 'query' : query}
                self.names[qname].append(newQuery)

    def get_data(self):
        return self.names

    def get_file(self):
        return self.f

    def reset(self):
        self.names.clear()
