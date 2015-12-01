import unittest
import StringIO

from packetsexample import PacketsExample
from prers import QtypeVSTld


class TestQtypeVSQnamelen(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = QtypeVSTld(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()
        for i in range(50):
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.nic.cl.', 'qtype': 1}]})
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.uchile.cl.', 'qtype': 2}]})

        for i in range(50):
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.google.com.', 'qtype': 1}]})
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.facebook.com.', 'qtype': 2}]})

        data.add_packet({'flags': '0', 'queries': [
                        {'qname': 'www.asdf.net.', 'qtype': 3}]})
        data.add_packet({'flags': '0', 'queries': [
                        {'qname': 'www.qwerty.net.', 'qtype': 3}]})

        data.set_expected(1, {'cl': 50, 'com': 50})
        data.set_expected(2, {'cl': 50, 'com': 50})
        data.set_expected(3, {'net': 2})

        data.put_information('QtypeVSTld', [1, 2, 3])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qvst in example.get_information('QtypeVSTld'):
            self.assertTrue(qvst in result)
            self.assertEquals(example.expected_value(qvst), result[qvst])
