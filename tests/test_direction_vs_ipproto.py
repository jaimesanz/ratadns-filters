import unittest
import StringIO

from packetsexample import PacketsExample
from prers import DirectionVSIpproto


class TestDirectionVSIpproto(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = DirectionVSIpproto(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()
        for i in range(30):
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.nic.cl.'}]})
            data.add_packet({'flags': '8000', 'queries': [
                            {'qname': 'www.crecemujer.cl.'}]})

        for i in range(25):
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.uchile.cl.'}]})

        for i in range(12):
            data.add_packet({'flags': '8000', 'queries': [
                            {'qname': 'www.facebook.com.'}]})

        data.set_expected('recv', {'udp': 55})
        data.set_expected('sent', {'udp': 42})

        data.put_information('DirectionVSIpproto', ['recv', 'sent'])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qvst in example.get_information('DirectionVSIpproto'):
            self.assertTrue(qvst in result)
            self.assertEquals(example.expected_value(qvst), result[qvst])
