from prers.prer import PreR

__author__ = 'franchoco'


class PacketSummary(PreR):

    def __init__(self, f):
        PreR.__init__(self, f)
        # Necesito acumular por QTYPE y luego por IP SRC
        self._acc = {}

    def __call__(self, p):
        """
        :type p: core.Packet
        """
        if p.is_answer():
            return

        if p.source in self._acc:
            if p.qtype in self._acc[p.source]:
                self._acc[p.source][p.qtype].append(p.qname)
            else:
                self._acc[p.source][p.qtype] = [p.qname]
        else:
            self._acc[p.source] = {p.qtype: [p.qname]}

    def get_data(self):
        return self._acc

    def reset(self):
        self._acc = {}
