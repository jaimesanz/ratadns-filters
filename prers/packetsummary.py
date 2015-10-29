from prers.prer import PreR

__author__ = 'franchoco'


class PacketSummary(PreR):
    def __init__(self, f):
        PreR.__init__(self, f)
        # Necesito acumular por QTYPE y luego por IP SRC
        self.acc = {}

    def __call__(self, p):
        """
        :type p: core.Packet
        """
        if p.is_answer():
            return

        if p.qtype in self.acc:
            if p.source in self.acc[p.qtype]:
                self.acc[p.qtype][p.source].append(p.qname)
            else:
                self.acc[p.qtype][p.source] = [p.qname]
        else:
            self.acc[p.qtype] = {p.source: [p.qname]}

    def get_data(self):
        return self.acc


    def reset(self):
        self.acc = {}
