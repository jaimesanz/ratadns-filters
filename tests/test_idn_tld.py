# -*- coding: utf-8 -*-

import unittest
import StringIO

from packetsexample import PacketsExample
from prers import IdnVSTld


class TestIdnVSTld(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__p1 = IdnVSTld(self.__stringbuffer1)

    def data_example(self):
        data = PacketsExample()
        for i in range(30):
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.nic.cóm.'}]})
            data.add_packet({'flags': '0', 'queries': [
                            {'qname': 'www.uchile.cl.'}]})

        data.set_expected(unicode('cóm', "utf8").encode("idna"), 30)

        data.put_information(
            'IdnVSTld', [
                unicode(
                    'cóm', "utf8").encode("idna")])

        return data

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qvst in example.get_information('IdnVSTld'):
            self.assertTrue(qvst in result)
            self.assertEquals(example.expected_value(qvst), result[qvst])
