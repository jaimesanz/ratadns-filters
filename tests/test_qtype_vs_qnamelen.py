import unittest
import StringIO

from packetsexample import PacketsExample
from prers import QtypeVSQnamelen


class TestQtypeVSQnamelen(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = QtypeVSQnamelen(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()
        data.add_packet({'flags': '0', 'queries': [
                        {'qname': 'www.nic.cl', 'qtype': 1}]})
        data.add_packet({'flags': '0', 'queries': [
                        {'qname': 'www.uchile.cl', 'qtype': 1}]})
        data.add_packet({'flags': '0', 'queries': [
                        {'qname': 'www.123456.cl', 'qtype': 2}]})
        data.add_packet({'flags': '0', 'queries': [
                        {'qname': 'www.123.cl', 'qtype': 1}]})
        data.add_packet({'flags': '0', 'queries': [
                        {'qname': 'dcc.uchile.cl', 'qtype': 1}]})
        data.add_packet({'flags': '0', 'queries': [
                        {'qname': 'www.niclabs.cl', 'qtype': 2}]})
        data.add_packet({'flags': '0', 'queries': [
                        {'qname': 'a.cl', 'qtype': 3}]})
        data.add_packet({'flags': '0', 'queries': [
                        {'qname': 'b.cl', 'qtype': 3}]})

        data.set_expected(1, {10: 2, 13: 2})
        data.set_expected(2, {13: 1, 14: 1})
        data.set_expected(3, {4: 2})

        data.put_information('QtypeVSQnamelen', [1, 2, 3])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qvsq in example.get_information('QtypeVSQnamelen'):
            self.assertTrue(qvsq in result)
            self.assertEquals(example.expected_value(qvsq), result[qvsq])
