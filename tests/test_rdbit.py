import unittest
import StringIO

from packetsexample import PacketsExample
from prers import RdBit


class TestRdBit(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = RdBit(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()

        for i in range(5):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.nic.cl'}]})

        data.set_expected("set", 5)
        data.set_expected("clr", 0)

        data.put_information('rdBit', ["set", "clr"])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for rdbit in example.get_information('rdBit'):
            self.assertTrue(rdbit in result)
            self.assertEquals(example.expected_value(rdbit), result[rdbit])
