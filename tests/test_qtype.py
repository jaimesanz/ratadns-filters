import unittest
import StringIO

from packetsexample import PacketsExample
from prers import Qtype


class TestQtype(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = Qtype(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()

        for i in range(5):
            data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.ni_c.cl', 'qtype': '1'}]})
       
        data.set_expected('1', 5)

        data.put_information("Qtype", ['1'])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qtype in example.get_information('Qtype'):
            self.assertTrue(qtype in result)
            self.assertEquals(example.expected_value(qtype), result[qtype])