__author__ = 'sking32'
from prer import PreR
class OnlyAnswers(PreR):
    """Show the answers in a window.

    - Result

    List of the answers in the current window

    - Example

    [{"id":"d4cf","flags":"8000"},
    {"id":"b767","flags":"8000"},
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
        flags =  int(d['flags'], 16)
    	is_answer = (flags & ( 1 << 15 )) == (1 << 15)
        if is_answer:
            self.l.append(d)
    def get_data(self):
        return self.l
    def reset(self):
        self.l = []
