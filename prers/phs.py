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

    def __call__(self, p):
        if not p.is_answer():
            qname = p.qname
            if "_" in qname and p.isCriticalType():
                sender = p.source
                query = p.query
                if self.names.has_key(sender):
                    self.names[sender]['cnt'] += 1
                    self.names[sender]['queries'].append(query)
                else:
                    self.names[sender] = {'cnt': 1, 'queries': [query]}

    def get_data(self):
        return self.names

    def reset(self):
        self.names.clear()
