import unittest
import StringIO

from packetsexample import PacketsExample
from prers import Opcode


class TestRcode(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = Opcode(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()

        for i in range(5):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.nic.cl'}]})

        data.set_expected(0, 5)

        data.put_information("Opcode", [0])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for opcode in example.get_information('Opcode'):
            self.assertTrue(opcode in result)
            self.assertEquals(example.expected_value(opcode), result[opcode])
