__author__ = 'sking32'
from prer import PreR
from core.packet import Packet
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

    def __call__(self, p):
        if not p.is_answer():
            query = p.queries[0]
            sender = p.source
            server = p.dest
            qname = p.qname()
            if "_" in qname and p.isCriticalType():
                if not self.names.has_key(qname):
                    self.names[qname] = []
                newQuery = {'sender': sender, 'server': server, 'query' : query}
                self.names[qname].append(newQuery)

    def get_data(self):
        return self.names

    def reset(self):
        self.names.clear()
