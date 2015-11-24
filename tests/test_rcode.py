import unittest
import StringIO

from packetsexample import PacketsExample
from prers import Rcode


class TestRcode(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = Rcode(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()

        for i in range(5):
            data.add_packet({'flags': '8000', 'queries': [
                {'qname': 'www.nic.cl'}]})
       
        data.set_expected(0, 5)

        data.put_information("Rcode", [0])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for rcode in example.get_information('Rcode'):
            self.assertTrue(rcode in result)
            self.assertEquals(example.expected_value(rcode), result[rcode])