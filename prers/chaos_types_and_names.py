from prer import PreR


class ChaosTypesAndNames(PreR):

    """Shows the count of the different queries grouped by qtype received on each packet with the same qname
    and with qclass 3 (chaos class)

    - Result
    
    A dict that has an entry for each qtype seen in a window. The key
    is the qtype and the value is another dictionary, which keys
    are the qnames and its value is the count of packets having that qname.
    - Example

    {
        1:
            {

                "www.uchile.cl": 10,
                "www.nic.cl": 1 
            },
        29: 
            {
                "www.facebook.com": 50
            }
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

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
                    
            self._chaos_types_and_names[qtype][qname] += 1

    def get_data(self):
    	return self._chaos_types_and_names

    def reset(self):
        self._chaos_types_and_names.clear()
