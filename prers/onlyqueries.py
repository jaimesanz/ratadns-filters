__author__ = 'franchoco'
from prer import PreR
class OnlyQueries(PreR):
    """Show the queries in a window.

    - Result

    List of the queries in the current window

    - Example

    [{"id":"d4cf","flags":"0"},
    {"id":"b767","flags":"0"},
    ...]

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """
    def __init__(self, f):
        PreR.__init__(self, f)
        self.l = []
    def __call__(self, d):
        #flags = d['flags']
	flags =  int(d['flags'], 16)
    	is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        #print str(flags)
	if not is_answer:
            self.l.append(d)
    def get_data(self):
        return self.l
    def reset(self):
        self.l = []
