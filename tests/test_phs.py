import unittest
import StringIO

from packetsexample import PacketsExample
from prers import PacketHasUnderscore
from core import Packet


class TestPacketHasUnderscore(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__stringbuffer2 = StringIO.StringIO()
        self.__p1 = PacketHasUnderscore(self.__stringbuffer1)
        self.__p2 = PacketHasUnderscore(self.__stringbuffer2)

    def data_example(self):

        data = PacketsExample()
        data.put_information('problematicSources', {
            'encrypted(ip1)':
                [{'qname': 'www.ni_c.cl', 'qtype': '1'}],
            'encrypted(ip2)':
                [{'qname': 'www.nic_labs.cl', 'qtype': '2'}],
            'encrypted(ip3)':
                [{'qname': 'www._jerry_.cl', 'qtype': '6'}],
            'encrypted(ip4)':
                [{'qname': 'www._pinky.cl', 'qtype': 'f'}]})

        # Problems with qnames
        data.add_packet({'source': 'encrypted(ip1)', 'flags': '0', 'queries': [
            {'qname': 'www.ni_c.cl', 'qtype': '1'}]})
        data.set_expected('encrypted(ip1)',  {"cnt": 1, 'queries': [
            {'qname': 'www.ni_c.cl', 'qtype': '1'}]})

        data.add_packet({'source': 'encrypted(ip2)', 'flags': '0', 'queries': [
            {'qname': 'www.nic_labs.cl', 'qtype': '2'}]})
        data.set_expected('encrypted(ip2)',  {"cnt": 1, 'queries': [
            {'qname': 'www.nic_labs.cl', 'qtype': '1'}]})

        data.add_packet({'source': 'encrypted(ip3)', 'flags': '0', 'queries': [
            {'qname': 'www._jerry_.cl', 'qtype': '6'}]})
        data.set_expected('encrypted(ip3)',  {"cnt": 1, 'queries': [
            {'qname': 'www._jerry_.cl', 'qtype': '1'}]})

        data.add_packet({'source': 'encrypted(ip4)', 'flags': '0', 'queries': [
            {'qname': 'www._pinky.cl', 'qtype': 'f'}]})
        data.set_expected('encrypted(ip4)',  {"cnt": 1, 'queries': [
            {'qname': 'www._pinky.cl', 'qtype': '1'}]})

        # Normal data, critical qtypes
        data.add_packet({'source': 'encrypted(ip1)', 'flags': '0', 'queries': [
            {'qname': 'www.nic.cl', 'qtype': '1'}]})
        data.add_packet({'source': 'encrypted(ip2)', 'flags': '0', 'queries': [
            {'qname': 'www.niclabs.cl', 'qtype': '2'}]})
        data.add_packet({'source': 'encrypted(ip3)', 'flags': '0', 'queries': [
            {'qname': 'www.jerry.cl', 'qtype': '6'}]})
        data.add_packet({'source': 'encrypted(ip4)', 'flags': '0', 'queries': [
            {'qname': 'www.pinky.cl', 'qtype': 'f'}]})

        # Normal data
        data.add_packet({'source': 'encrypted(ip1)', 'flags': '0',
                         'queries': [{'qname': 'www.nic.cl', 'qtype': '3'}]})
        data.add_packet({'source': 'encrypted(ip2)', 'flags': '8000',
                         'queries': [{'qname': 'www.niclabs.cl',
                                      'qtype': '4'}]})
        data.add_packet({'source': 'encrypted(ip3)', 'flags': '0',
                         'queries': [{'qname': 'www.jerry.cl', 'qtype': '5'}]})
        data.add_packet({'source': 'encrypted(ip4)', 'flags': '8000',
                         'queries': [{'qname': 'www.pinky.cl',
                                      'qtype': '7'}]})

        # Underscore data, noncritical qtypes
        data.add_packet({'source': 'encrypted(ip1)', 'flags': '0',
                         'queries': [{'qname': 'www.ni_c.cl', 'qtype': '3'}]})
        data.add_packet({'source': 'encrypted(ip2)', 'flags': '0',
                         'queries': [{'qname': 'www.nic_labs.cl',
                                      'qtype': '4'}]})
        data.add_packet({'source': 'encrypted(ip3)', 'flags': '0',
                         'queries': [{'qname': 'www._jerry_.cl',
                                      'qtype': '5'}]})
        data.add_packet({'source': 'encrypted(ip4)', 'flags': '0',
                         'queries': [{'qname': 'www._pinky.cl',
                                      'qtype': '7'}]})

        # Answers
        data.add_packet({'source': 'encrypted(dnsip1)', 'flags': '8000',
                         'queries': [{'qname': 'www.ni_c.cl',
                                      'qtype': '1'}]})
        data.add_packet({'source': 'encrypted(dnsip2)', 'flags': '8000',
                         'queries': [{'qname': 'www.niclabs.cl',
                                      'qtype': '2'}]})
        data.add_packet({'source': 'encrypted(dnsip3)', 'flags': '8000',
                         'queries': [{'qname': 'www.jerry.cl',
                                      'qtype': '5'}]})
        data.add_packet({'source': 'encrypted(dnsip4)', 'flags': '8000',
                         'queries': [{'qname': 'www._pinky.cl',
                                      'qtype': '7'}]})

        return data

    def data_repeat_error(self):
        data = PacketsExample()

        data.put_information('problematicSources', {
            'encrypted(ip1)': [{'qname': 'www.ni_c.cl', 'qtype': '1'}],
            'encrypted(ip2)': [{'qname': 'www.nic_labs.cl', 'qtype': '2'}]})

        count_of_errors = {}

        for i in range(3):
            data.add_packet({'source': 'encrypted(ip1)', 'flags': '0',
                             'queries': [{'qname': 'www.ni_c.cl',
                                          'qtype': '1'}]})
        count_of_errors['encrypted(ip1)'] = 3

        for i in range(2):
            data.add_packet({'source': 'encrypted(ip2)', 'flags': '0',
                             'queries': [{'qname': 'www.nic_labs.cl',
                                          'qtype': '2'}]})
        count_of_errors['encrypted(ip2)'] = 2

        data.put_information('countOfErrors', count_of_errors)
        return data

    def setUp(self):
        self.reinit()

    def test_right_format(self):
        self.reinit()

        self.__p1(Packet({'source': 'encrypted(ip1)', 'flags': '0',
                          'queries': [{'qname': 'www.ni_c.cl',
                                       'qtype': '1'}]}))
        result = self.__p1.get_data()

        self.assertEquals(type(result), dict)

        result_for_source = result['encrypted(ip1)']
        self.assertEquals(type(result_for_source), dict)
        self.assertTrue('cnt' in result_for_source)
        self.assertTrue('queries' in result_for_source)

        self.assertGreater(result_for_source['cnt'], 0)

        queries = result_for_source['queries']
        self.assertEquals(type(queries), list)
        self.assertGreater(len(queries), 0)

        query_example = queries[0]
        self.assertTrue('qtype' in query_example)
        self.assertTrue('qname' in query_example)

    def test_no_data(self):
        self.reinit()

        result = self.__p1.get_data()

        self.assertEquals({}, result)

    def test_same_behavior(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)
        for packet in example:
            self.__p2(packet)

        result1 = self.__p1.get_data()
        result2 = self.__p2.get_data()

        self.assertTrue(result1, result2)

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        expected_problematic = example.get_information('problematicSources')

        for source in result.keys():
            self.assertTrue(source in expected_problematic)

        for source in expected_problematic.keys():
            self.assertTrue(source in result)
            expected_queries = expected_problematic[source]
            self.assertEquals(len(expected_queries), result[source]['cnt'])
            self.assertEquals(len(expected_queries),
                              len(result[source]['queries']))
            self.assertListEqual(expected_queries, result[source]['queries'])

    def test_data_repeat_error(self):
        self.reinit()

        example = self.data_repeat_error()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        expected_problematic = example.get_information('problematicSources')
        expected_cnt = example.get_information('countOfErrors')

        for source in expected_problematic.keys():
            self.assertTrue(source in result)
            expected_queries = expected_problematic[source]
            self.assertEquals(expected_cnt[source], result[source]['cnt'])
            self.assertEquals(result[source]['cnt'],
                              len(result[source]['queries']))
            for query in result[source]['queries']:
                self.assertEqual(expected_queries[0], query)

    def test_reset(self):
        self.reinit()

        example = self.data_example()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()
            expected_problematic = example.get_information(
                'problematicSources')

            for source in result.keys():
                self.assertTrue(source in expected_problematic)

            for source in expected_problematic.keys():
                self.assertTrue(source in result)
                expected_queries = expected_problematic[source]
                self.assertEquals(len(expected_queries), result[source]['cnt'])
                self.assertListEqual(expected_queries, result[
                                     source]['queries'])

            self.__p1.reset()

    def test_file(self):
        self.reinit()

        self.assertEquals(self.__stringbuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
