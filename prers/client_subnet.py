from prer import PreR
from core import get_topk_with_skipped_count_1D

class ClientSubnet(PreR):
    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._client_subnet = {}
        self._k = 200

    def __call__(self, p):
        if not p.is_answer():
            if p.source not in self._client_subnet:
                self._client_subnet[p.source] = 0
            self._client_subnet[p.source] += 1

    def get_data(self):
        return get_topk_with_skipped_count_1D(self._client_subnet,self._k)

    def reset(self):
        self._client_subnet.clear()