import unittest
import StringIO

from packetsexample import PacketsExample
from prers import CertainQnamesVSQtype


class TestCertainQnamesVSQtype(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = CertainQnamesVSQtype(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()
        for i in range(30):
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'localhost.', 'qtype': 1}]})
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'localhost.', 'qtype': 2}]})
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'x.root-servers.net.', 'qtype': 2}]})

        for i in range(25):
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.uchile.cl.', 'qtype': 3}]})
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'asdf.root-servers.net.', 'qtype': 3}]})

        data.set_expected('localhost', {1: 30, 2: 30})
        data.set_expected('root-servers.net', {2: 30, 3: 25})
        data.set_expected('else', {3: 25})

        data.put_information(
            'CertainQnamesVSQtype', [
                'localhost', 'root-servers.net', 'else'])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qvst in example.get_information('CertainQnamesVSQtype'):
            self.assertTrue(qvst in result)
            self.assertEquals(example.expected_value(qvst), result[qvst])
