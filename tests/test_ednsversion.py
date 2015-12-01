import unittest
import StringIO

from packetsexample import PacketsExample
from prers import EdnsVersion


class TestEdnsVersion(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = EdnsVersion(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()

        for i in range(5):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.nic.cl'}]})

        data.set_expected(0, 5)

        data.put_information("EdnsVersion", [0])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for ednsversion in example.get_information('EdnsVersion'):
            self.assertTrue(ednsversion in result)
            self.assertEquals(
                example.expected_value(ednsversion),
                result[ednsversion])
