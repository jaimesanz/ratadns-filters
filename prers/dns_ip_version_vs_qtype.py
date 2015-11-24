from core import is_ipv4
from prer import PreR


class DnsIpVersionVSQtype(PreR):

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._dns_ip_version_vs_qtype = {'IPv4':{},'IPv6':{}}

    def __call__(self, p):

        if not p.is_answer():
            ip = 'IPv4' if is_ipv4(p.source) else 'IPv6'  
            if p.qtype not in self._dns_ip_version_vs_qtype[ip]:
                self._dns_ip_version_vs_qtype[ip][p.qtype] = 0
            self._dns_ip_version_vs_qtype[ip][p.qtype] += 1

    def get_data(self):
    	return self._dns_ip_version_vs_qtype

    def reset(self):
        self._dns_ip_version_vs_qtype = {'IPv4':{},'IPv6':{}}
