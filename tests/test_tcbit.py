import unittest
import StringIO

from packetsexample import PacketsExample
from prers import TcBit


class TestTcBit(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = TcBit(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()

        for i in range(5):
            data.add_packet({'flags': '8000', 'queries': [
                {'qname': 'www.nic.cl'}]})

        data.set_expected("set", 0)
        data.set_expected("clr", 5)

        data.put_information('tcBit', ["set", "clr"])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for tcbit in example.get_information('tcBit'):
            self.assertTrue(tcbit in result)
            self.assertEquals(example.expected_value(tcbit), result[tcbit])
