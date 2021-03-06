from prer import PreR


class QueriesWithUnderscoredName(PreR):
    """Group the queries in a window which qtype are in
    {1, 2, 6, 15} and its qnames have an underscore by the qname

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
        self._names = {}

    def __call__(self, p):
        if not p.is_answer():
            query = p.query
            sender = p.source
            server = p.dest
            qname = p.qname
            if "_" in qname and p.is_critical_type():
                if qname not in self._names:
                    self._names[qname] = []
                newQuery = {'sender': sender, 'server': server, 'query': query}
                self._names[qname].append(newQuery)

    def get_data(self):
        return self._names

    def reset(self):
        self._names.clear()
