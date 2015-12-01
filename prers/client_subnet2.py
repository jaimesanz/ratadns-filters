from core import get_topk_with_skipped_count_2D, hex_to_ip
from prer import PreR


class ClientSubnet2(PreR):
    """Shows the count of the different client addresses of each query in a window
    with the same bogus query classification.

    Bogus query classification:

        non-auth-tld: when the TLD is not one of the IANA-approved TLDs.
        root-servers.net: a query for a root server IP address.
        localhost: a query for the localhost IP address.
        a-for-root: an A query for the DNS root (.).
        a-for-a: an A query for an IPv4 address.
        rfc1918-ptr: a PTR query for an RFC 1918 address.
        funny-class: a query with an unknown/undefined query class.
        funny-qtype: a query with an unknown/undefined query type.
        src-port-zero: when the UDP message's source port equals zero.
        malformed: a malformed DNS message that could not be entirelyparsed.
        ok: not bogus.

    - Result
    
    A dict that has an entry for each different bogus query classification seen in a window.
    The key is the classification (string) and the value is another dictionary, which keys
    are the ip addresses of the clients (hex) and their values are the count of packets
    having that ip. If there are more than 50 addresses with one same class, it 
    will only show the top 200 addresses and two other keys will be added to the 
    dictionary:
         "-:SKIPPED:-" -> the amount of client addresses it's not showing
         "-:SKIPPED_SUM:-:" -> the sum of the count of all the client addresses
         it's not showing

    - Example

    {
        "non-auth-tld":
            {
                AABBCCDD: 50,
                AABBCCDA: 10,
                -:SKIPPED:-: 1,
                -:SKIPPED_SUM:-:7
            },
        "ok": 
            {
                AABBCCBB: 50
            }
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._client_subnet2 = {}
        self._k = 200

    def __call__(self, p):
        if not p.is_answer():
            is_ok=True
            source_ip = p.source
            if self.is_non_auth_tld(p):
                # non-auth-tld: when the TLD is not one of the IANA-approved TLDs.
                self.incr_count("non-auth-tld", source_ip)
                is_ok=False

            if p.qname.endswith("root-servers.net."):
                # root-servers.net: a query for a root server IP address.
                self.incr_count("root-servers.net", source_ip)
                is_ok=False
            if p.qname=="localhost.":
                # localhost: a query for the localhost IP address.
                self.incr_count("localhost", source_ip)
                is_ok=False
            if p.qtype==1 and p.qname==".":
                # a-for-root: an A query for the DNS root (.).
                self.incr_count("a-for-root", source_ip)
                is_ok=False
            if p.qtype==1 and len(p.dest)==8:
                # a-for-a: an A query for an IPv4 address.
                self.incr_count("a-for-a", source_ip)
                is_ok=False

            if self.is_rfc1918_ptr(p):
                # rfc1918-ptr: a PTR query for an RFC 1918 address.
                self.incr_count("rfc1918-ptr", source_ip)
                is_ok=False

            if self.is_funny_class(p):
                # funny-class: a query with an unknown/undefined query class.
                self.incr_count("funny-class", source_ip)
                is_ok=False
            if self.is_funny_qtype(p):
                # funny-qtype: a query with an unknown/undefined query type.
                self.incr_count("funny-qtype", source_ip)
                is_ok=False
            if p.source_port==0 and p.transport_protocol == "udp":
                # src-port-zero: when the UDP message's source port equals zero.
                self.incr_count("src-port-zero", source_ip)
                is_ok=False
            # if is_malformed(p): NOT IMPLEMENTED: this can't be done because rata filters malformed queries, so they never get to this point of the process
            if is_ok:
                # ok: not bogus.
                self.incr_count("ok", source_ip)

    def incr_count(self, bogus_type, source_ip):
        if bogus_type not in self._client_subnet2:
            self._client_subnet2[bogus_type]={}
        if source_ip not in self._client_subnet2[bogus_type]:
            self._client_subnet2[bogus_type][source_ip]=0
        self._client_subnet2[bogus_type][source_ip]+=1
    
    def get_data(self):
        return get_topk_with_skipped_count_2D(self._client_subnet2, self._k)

    def reset(self):
        self._client_subnet2.clear()

    def is_non_auth_tld(self,p):
        # IMPORTANT: data/iana_approved_tlds.txt must be updated from https://data.iana.org/TLD/tlds-alpha-by-domain.txt daily
        with open('prers/data/iana_approved_tlds.txt') as f:
            approved_tlds = [line.rstrip() for line in f][1:]
            qname = p.qname
            tld = qname.split(".")[-2]
            return tld.upper() not in approved_tlds

    def is_funny_class(self,p):
        # reference http://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml#dns-parameters-2
        # 2, 5-253, 256-65279
        with open('prers/data/funny_classes.txt') as f:
            funny_classes = [line.rstrip() for line in f]
            qclass = p.qclass
            return qclass in funny_classes

    def is_funny_qtype(self,p):
        with open('prers/data/iana_approved_qtypes.txt') as f:
            approved_qtypes = [line.rstrip() for line in f]
            return str(p.qtype) not in approved_qtypes

    def is_rfc1918_ptr(self,p):
        if len(p.dest)>8:
            return False
        ip = hex_to_ip(p.dest)
        dest_ip = [int(n) for n in ip.split(".")]

        # RFC 1918 addresses
        # 10.0.0.0 - 10.255.255.255  (10/8 prefix)
        range1 = (dest_ip[0]==10)
        # 172.16.0.0 - 172.31.255.255  (172.16/12 prefix)
        range2 = (dest_ip[0]==172 and dest_ip[1]>=16 and dest_ip[1]<=31)
        # 192.168.0.0 - 192.168.255.255 (192.168/16 prefix)
        range3 = (dest_ip[0]==192 and dest_ip[1]==168)

        return p.qtype==12 and (range1 or range2 or range3)