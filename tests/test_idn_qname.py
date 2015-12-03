# -*- coding: utf-8 -*-

import unittest
import StringIO

from packetsexample import PacketsExample
from prers import IdnQname


class TestIdnQname(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = IdnQname(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()
        for i in range(30):
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.xn--nand-tra.cl.'}]})
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.xn--andu-fqa.cl.'}]})

        for i in range(25):
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.uchile.cl.'}]})

        data.set_expected('normal', 25)
        data.set_expected('idn', 60)

        data.put_information('IdnQname', ['normal', 'idn'])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qvst in example.get_information('IdnQname'):
            self.assertTrue(qvst in result)
            self.assertEquals(example.expected_value(qvst), result[qvst])
