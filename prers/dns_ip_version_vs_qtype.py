from core import is_ipv4
from prer import PreR


class DnsIpVersionVSQtype(PreR):


	def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._dns_ip_version_vs_qtype = {}

    def __call__(self, p):
        if is_ipv4(p.source):
            if "IPv4" not in self._dns_ip_version_vs_qtype:
                self._dns_ip_version_vs_qtype["IPv4"]=0
            self._dns_ip_version_vs_qtype["IPv4"]+=1
        else:
            if "IPv6" not in self._dns_ip_version_vs_qtype:
                self._dns_ip_version_vs_qtype["IPv6"]=0
            self._dns_ip_version_vs_qtype["IPv6"]+=1

    def get_data(self):
    	return self._dns_ip_version_vs_qtype

    def reset(self):
        self._dns_ip_version_vs_qtype.clear()