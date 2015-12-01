import unittest
import StringIO

from packetsexample import PacketsExample
from prers import ClientAddrVSRcode


class TestClientAddrVSRcode(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = ClientAddrVSRcode(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()
        for i in range(30):
            data.add_packet({'flags': '8000',
                             'source': '12345678',
                             'queries': [{'qname': 'www.nic.cl.'}]})

        for i in range(12):
            data.add_packet({'flags': '8000', 'source': '87654321',
                            'queries': [{'qname': 'www.niclabs.cl.'}]})

        for i in range(25):
            data.add_packet({'flags': '8000',
                             'source': '12348765',
                             'queries': [{'qname': 'www.uchile.cl.'}]})

        data.set_expected(0, {'12345678': 30, '87654321': 12, '12348765': 25})

        data.put_information('ClientAddrVSRcode', [0])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qvst in example.get_information('ClientAddrVSRcode'):
            self.assertTrue(qvst in result)
            self.assertEquals(example.expected_value(qvst), result[qvst])
