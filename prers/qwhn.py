__author__ = 'sking32'
from prer import PreR

class QueriesWithUnderscoredName(PreR):
    """Group the queries in a window which qtype are in {1, 2, 6, 15} and its qnames have an underscore by the qname

    - Result

    Dict which keys are qnames
    with an underscore and the value is a list
    of dicts showing the sender, server and query
    for the queries with this qname

    - Example

    {"www.pin_ky.cl": [
    {"query": {"qclass": "1", "qtype": "6", "qname": "www.Pin_kY.cl"},
    "sender": "c81c0481",
    "server": "c8070407"},
    ... ]}

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """
    def __init__(self, f):
        PreR.__init__(self, f)
        self.names = {}

    def __call__(self, d):
        flags =  int(d['flags'], 16)
        is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        if not is_answer:
            query = d['queries'][0]
            qname = query['qname'].lower()
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

    def reset(self):
        self.names.clear()