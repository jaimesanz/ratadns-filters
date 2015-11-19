from core import is_ipv4
from prer import PreR


class dns_ip_version_vs_qtype(PreR):


	def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._dns_ip_version_vs_qtype = {}

    def __call__(self, p):

        # <IPVersion val="IPv6">
        #     <Qtype count="81332" val="24"/>
        #     <Qtype count="17846" val="25"/>
        # </IPVersion>
        # <IPVersion val="IPv4">
        #     <Qtype count="81332" val="2"/>
        #     <Qtype count="17846" val="255"/>
        # </IPVersion>

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