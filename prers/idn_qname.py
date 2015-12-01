from encodings import idna
from prer import PreR


class IdnQname(PreR):
    """Shows the count of the internationalized domain name queries received in
    a window.

    - Result

    A dict that has two entries: 'normal' (which has the count of normal domain
    names) and 'idn' (which has the count of internationalized domain names)

    - Example

    {
        'normal': 60, # vanilla domain names
        'idn': 10 # internationalized domain names
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._idn_qname = {"normal": 0, "idn": 0}

    def __call__(self, p):
        if not p.is_answer():
            qname = p.qname
            try:
                idna.ToASCII(qname)
                # if this fails, it means this is NOT a normal domain name (for
                # instance, it has a weird character)
                self._idn_qname["normal"] += 1
            except Exception as e:
                self._idn_qname["idn"] += 1

    def get_data(self):
        return self._idn_qname

    def reset(self):
        self._idn_qname["idn"] = 0
        self._idn_qname["normal"] = 0
