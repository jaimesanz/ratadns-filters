__author__ = 'sking32'

#The result is a dict which has the queries, answers
# and a list of the alone packets(queries without answers and
# answers without queries)
class AlonePackets(object) :
    def __init__(self, f):
        self.qcounter = 0
        self.acounter = 0
        self.f = f
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

    def get_file(self):
        return self.f

    def reset(self):
        self.pcounter = self.qcounter = self.acounter = self.alpcounter = self.alqcounter = self.alacounter = 0
        self.aloneQueriesIds = {} #Dicts {id : InputDict}
        self.aloneAnswersIds = {}

