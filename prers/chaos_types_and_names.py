from prer import PreR


class chaos_types_and_names(PreR):


	def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._chaos_types_and_names = {}

    def __call__(self, p):

    	if (not p.is_answer()) and (p.qclass == 3):
            qtype = p.qtype
            qname = p.qname

            if qtype not in self._chaos_types_and_names:
                self._chaos_types_and_names[qtype] = {}
            
            if qname not in self._chaos_types_and_names[qtype]:
                self._chaos_types_and_names[qtype][qname] = 0
                    
            self._chaos_types_and_names[qtype][qname]+=1

    def get_data(self):
    	return self._chaos_types_and_names

    def reset(self):
        self._chaos_types_and_names.clear()
