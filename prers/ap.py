__author__ = 'sking32'
from prer import PreR
from core.packet import Packet


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
        self.aloneQueriesIds = {}  # Dicts {id : InputDict}
        self.aloneAnswersIds = {}

    def __call__(self, p):
        if p.is_answer():
            self.acounter += 1
            if self.aloneQueriesIds.has_key(p.id):
                self.aloneQueriesIds.pop(p.id, None)
            else:
                self.aloneAnswersIds[p.id] = p.input

        else:
            self.qcounter += 1
            if self.aloneAnswersIds.has_key(p.id):
                self.aloneAnswersIds.pop(p.id, None)
            else:
                self.aloneQueriesIds[p.id] = p.input

    def get_data(self):
        data = {'queries': self.qcounter, 'answers': self.acounter, 'AloneAnswers': self.aloneAnswersIds.values(),
                'AloneQueries': self.aloneQueriesIds.values()}
        return data

    def reset(self):
        self.pcounter = self.qcounter = self.acounter = self.alpcounter = self.alqcounter = self.alacounter = 0
        self.aloneQueriesIds = {}  # Dicts {id : Input}
        self.aloneAnswersIds = {}
