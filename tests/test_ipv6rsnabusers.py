import unittest
import StringIO

from packetsexample import PacketsExample
from prers import Ipv6RsnAbusers

class TestRcode(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = Ipv6RsnAbusers(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()

        for i in range(5):
            data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'a-root-servers.net.', 'qtype': '1'}]})
       
        data.set_expected("encrypted(ip1)", 5)

        data.put_information("src", ["encrypted(ip1)"])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for src in example.get_information('src'):
            self.assertTrue(src in result)
            self.assertEquals(example.expected_value(src), result[src])