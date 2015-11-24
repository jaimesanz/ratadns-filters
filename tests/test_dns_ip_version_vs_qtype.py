import unittest
import StringIO

from packetsexample import PacketsExample
from prers import DnsIpVersionVSQtype


class TestDnsIpVersionVSQtype(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = DnsIpVersionVSQtype(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()
        for i in range(30):
            data.add_packet({'flags': '0','source': '12345678','queries': [{'qname': 'www.nic.cl.','qtype':1}]})

        for i in range(12):
            data.add_packet({'flags': '0','source': '87654321','queries': [{'qname': 'www.niclabs.cl.','qtype': 2}]})
            data.add_packet({'flags': '0','source': '8765432100','queries': [{'qname': 'www.niclabs.cl.','qtype': 2}]})

        for i in range(25):
            data.add_packet({'flags': '0','source': '12348765','queries': [{'qname': 'www.uchile.cl.','qtype': 3}]})
            data.add_packet({'flags': '0','source': '1234876500','queries': [{'qname': 'www.uchile.cl.','qtype': 3}]})
            data.add_packet({'flags': '0','source': '12345678','queries': [{'qname': 'www.uchile.cl.','qtype': 3}]})


        data.set_expected('IPv4',{1: 30, 2: 12, 3: 50})
        data.set_expected('IPv6',{2: 12, 3: 25})

        data.put_information('DnsIpVersionVSQtype',['IPv4','IPv6'])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qvst in example.get_information('DnsIpVersionVSQtype'):
            self.assertTrue(qvst in result)
            self.assertEquals(example.expected_value(qvst), result[qvst])