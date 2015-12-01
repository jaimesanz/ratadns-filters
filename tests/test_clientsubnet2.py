import unittest
import StringIO

from packetsexample import PacketsExample
from prers import ClientSubnet2


class TestRcode(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = ClientSubnet2(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()

        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [{'qname': 'www.nic.notapprovedtld.',
                                      'qtype': 1}]})
        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [{'qname': 'a-root-servers.net.',
                                      'qtype': 1}]})
        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [{'qname': 'localhost.',
                                      'qtype': 1}]})
        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [{'qname': '.',
                                      'qtype': 1}]})
        data.add_packet({'dest': 'AABBCCDD', 'source': 'encrypted(ip1)',
                         'flags': '0', 'queries': [{'qname': 'www.nic.cl.', 'qtype': 1}]})
        data.add_packet({'dest': 'AC1FFFFF',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [{'qname': 'www.nic.cl.',
                                      'qtype': 12}]})
        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [{'qname': 'localhost.',
                                      'qtype': 134134345}]})
        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [{'qname': 'www.nic.cl.',
                                      'qtype': 1}]})

        data.set_expected("non-auth-tld", {'encrypted(ip1)': 4})
        data.set_expected("root-servers.net", {'encrypted(ip1)': 1})
        data.set_expected("localhost", {'encrypted(ip1)': 2})
        data.set_expected("a-for-root", {'encrypted(ip1)': 1})
        data.set_expected("a-for-a", {'encrypted(ip1)': 1})
        data.set_expected("rfc1918-ptr", {'encrypted(ip1)': 1})
        data.set_expected("funny-qtype", {'encrypted(ip1)': 1})
        data.set_expected("ok", {'encrypted(ip1)': 1})

        data.put_information("class",
                             ["non-auth-tld",
                              "root-servers.net",
                              "localhost",
                              "a-for-root",
                              "a-for-a",
                              "rfc1918-ptr",
                              "funny-qtype",
                              "ok"])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for cls in example.get_information('class'):
            self.assertTrue(cls in result)
            self.assertEquals(example.expected_value(cls), result[cls])
