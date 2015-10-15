__author__ = 'sking32'
from prer import PreR
class NullPreR(PreR):
    """Implements a default behavior for the null pattern.

    - Result

    None

    - Example

    None

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """
    def __init__(self, f):
        PreR.__init__(self,f)
    def __call__(self, p):
        pass
    def get_data(self):
        return None
    def reset(self):
        pass
