import unittest
import StringIO

from packetsexample import PacketsExample
from prers import TransportVSQtype


class TestTransportVSQtype(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = TransportVSQtype(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()
        for i in range(30):
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.nic.cl.', 'qtype': 1}]})
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.niclabs.cl.', 'qtype': 2}]})

        for i in range(25):
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.uchile.cl.', 'qtype': 3}]})

        data.set_expected('udp', {1: 30, 2: 30, 3: 25})

        data.put_information('TransportVSQtype', ['udp'])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qvst in example.get_information('TransportVSQtype'):
            self.assertTrue(qvst in result)
            self.assertEquals(example.expected_value(qvst), result[qvst])
