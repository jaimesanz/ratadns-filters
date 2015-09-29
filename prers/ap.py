__author__ = 'sking32'
from prer import PreR

class AlonePackets(PreR) :
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
        self.aloneQueriesIds = {} #Dicts {id : InputDict}
        self.aloneAnswersIds = {}

    def __call__(self, d):
        flags =  int(d['flags'], 16)
        id = d['id']
        is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        if is_answer:
            self.acounter += 1
            if self.aloneQueriesIds.has_key(id) :
                self.aloneQueriesIds.pop(id, None)
            else :
                self.aloneAnswersIds[id] = d

        else:
            self.qcounter += 1
            if self.aloneAnswersIds.has_key(id) :
                self.aloneAnswersIds.pop(id, None)
            else :
                self.aloneQueriesIds[id] = d
        
    def get_data(self):
        data = {'queries' : self.qcounter, 'answers' : self.acounter, 'AloneAnswers' : self.aloneAnswersIds.values(), 'AloneQueries' : self.aloneQueriesIds.values()}
        return data

    def reset(self):
        self.pcounter = self.qcounter = self.acounter = self.alpcounter = self.alqcounter = self.alacounter = 0
        self.aloneQueriesIds = {} #Dicts {id : InputDict}
        self.aloneAnswersIds = {}

