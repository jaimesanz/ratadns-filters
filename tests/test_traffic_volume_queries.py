import unittest
import StringIO

from packetsexample import PacketsExample
from prers import TrafficVolumeQueries


class TestTrafficVolumeQueries(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = TrafficVolumeQueries(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()
        for i in range(30):
            data.add_packet({'flags': '0', 'source': '12345678',
                             'queries': [{'qname': 'www.nic.cl.'}]})

        for i in range(25):
            data.add_packet({'flags': '0',
                             'source': '1234567890',
                             'queries': [{'qname': 'www.uchile.cl.'}]})

        data.set_expected('udp', {'IPv4': 30, 'IPv6': 25})

        data.put_information('TrafficVolumeQueries', ['udp'])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qvst in example.get_information('TrafficVolumeQueries'):
            self.assertTrue(qvst in result)
            self.assertEquals(example.expected_value(qvst), result[qvst])
