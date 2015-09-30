__author__ = 'franchoco'
from prer import PreR

class PacketHasUnderscore(PreR):
    """Group the queries in a window which qtype are in {1, 2, 6, 15} and its qnames have an underscore by the ipsource

    - Result

    Dict which keys are the ipsource that have 'problematic' queries
    and values are dicts that contains the number of 'problematic'
    queries from that source and the queries itself(in a list)

    - Example

    {"c81c0481": {"cnt": 2, "queries": [{...}, {...}]},
    {"a41c5361": {"cnt": 1, "queries": [{...}]}}

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

    def reset(self):
        self.names.clear()
