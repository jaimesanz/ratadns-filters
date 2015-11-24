import unittest
import StringIO

from packetsexample import PacketsExample
from prers import RcodeVSReplylen


class TestRcodeVSReplylen(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = RcodeVSReplylen(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()
        for i in range(30):
            data.add_packet({'flags': '8000','queries': [{'qname': 'www.nic.cl.'}]})
            data.add_packet({'flags': '0','queries': [{'qname': 'www.niclabs.cl.'}]})

        for i in range(25):
            data.add_packet({'flags': '8000','queries': [{'qname': 'www.uchile.cl.'}]})


        data.set_expected(0,{15: 55})

        data.put_information('RcodeVSReplylen',[0])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qvst in example.get_information('RcodeVSReplylen'):
            self.assertTrue(qvst in result)
            self.assertEquals(example.expected_value(qvst), result[qvst])