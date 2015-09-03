__author__ = 'sking32'

#The result is a dict which has the queries, answers
# and a list of the alone packets(queries without answers and
# answers without queries)
class AlonePackets(object) :
    def __init__(self, f):
        self.pcounter = 0
        self.qcounter = 0
        self.acounter = 0
        self.alpcounter = 0
        self.alqcounter = 0
        self.alacounter = 0
        self.f = f
        self.aloneQueriesIds = {} #Dicts {id : InputDict}
        self.aloneAnswersIds = {}
        self.alonePacketsIds = {}

    def __call__(self, d):
        flags =  int(d['flags'], 16)
        id = d['id']
        is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        self.pcounter += 1
        if is_answer:
            self.acounter += 1
            if self.aloneQueriesIds.has_key(id) :
                self.alonePacketsIds.pop(id, None)
                self.alpcounter -= 1
                self.aloneQueriesIds.pop(id, None)
                self.alqcounter -= 1
            else :
                self.alonePacketsIds[id] = d
                self.alpcounter += 1
                self.aloneAnswersIds[id] = d
                self.alacounter += 1

        else:
            self.qcounter += 1
            if self.aloneAnswersIds.has_key(id) :
                self.alonePacketsIds.pop(id, None)
                self.alpcounter -= 1
                self.aloneAnswersIds.pop(id, None)
                self.alacounter -= 1

            else :
                self.alonePacketsIds[id] = d
                self.alpcounter += 1
                self.aloneQueriesIds[id] = d
                self.alqcounter += 1

    def get_data(self):
        data = {'queries' : self.qcounter, 'answers' : self.acounter, 'AlonePackets' : self.alonePacketsIds.values()}
        return data

    def get_file(self):
        return self.f

    def reset(self):
        self.pcounter = self.qcounter = self.acounter = self.alpcounter = self.alqcounter = self.alacounter = 0
        self.aloneQueriesIds = {} #Dicts {id : InputDict}
        self.aloneAnswersIds = {}
        self.alonePacketsIds = {}

