from prer import PreR


class AlonePackets(PreR):
    """Show information about alone packets in a window

    - Result

    Dict which has the number of queries, number of answers
    and two lists, one for the queries without answers and
    another for answers without queries, in current the window

    - Example

    {'queries' : 12, 'answers' : 10, 'AloneAnswers' : [],
    'AloneQueries' : []}

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f):
        PreR.__init__(self, f)
        self.qcounter = 0
        self.acounter = 0
        self.alone_queries_ids = {}  # Dicts {id : InputDict}
        self.alone_answers_ids = {}

    def __call__(self, p):
        if p.is_answer():
            self.acounter += 1
            if p.id in self.alone_queries_ids:
                self.alone_queries_ids.pop(p.id, None)
            else:
                self.alone_answers_ids[p.id] = p.input

        else:
            self.qcounter += 1
            if p.id in self.alone_answers_ids:
                self.alone_answers_ids.pop(p.id, None)
            else:
                self.alone_queries_ids[p.id] = p.input

    def get_data(self):
        data = {'queries': self.qcounter, 'answers': self.acounter,
                'AloneAnswers': self.alone_answers_ids.values(),
                'AloneQueries': self.alone_queries_ids.values()}
        return data

    def reset(self):
        self.pcounter = self.qcounter = self.acounter\
            = self.alpcounter = self.alqcounter = self.alacounter = 0
        self.alone_queries_ids = {}  # Dicts {id : Input}
        self.alone_answers_ids = {}
