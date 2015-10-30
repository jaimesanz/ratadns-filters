import unittest
import StringIO

from packetsexample import PacketsExample
from prers.qwhn import QueriesWithUnderscoredName
from core import Packet


class TestQueriesWithUnderscoredName(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__stringbuffer2 = StringIO.StringIO()
        self.__p1 = QueriesWithUnderscoredName(self.__stringbuffer1)
        self.__p2 = QueriesWithUnderscoredName(self.__stringbuffer2)

    def data_example(self):

        data = PacketsExample()

        data.put_information('problematicQNames', {
            'www.ni_c.cl',
            'www.nic_labs.cl',
            'www._jerry_.cl',
            'www._pinky.cl'})

        # Problems with qnames
        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.ni_c.cl', 'qtype': '1'}]})
        data.set_expected('www.ni_c.cl',
                          [{'server': 'encrypted(dnsip1)',
                            'sender': 'encrypted(ip1)',
                            'query': {'qname': 'www.ni_c.cl', 'qtype': '1'}}])

        data.add_packet({'dest': 'encrypted(dnsip2)',
                         'source': 'encrypted(ip2)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.nic_labs.cl', 'qtype': '2'}]})
        data.set_expected('www.nic_labs.cl', [
            {'server': 'encrypted(dnsip2)',
             'sender': 'encrypted(ip2)',
             'query': {
                 'qname': 'www.nic_labs.cl', 'qtype': '2'}}])

        data.add_packet({'dest': 'encrypted(dnsip3)',
                         'source': 'encrypted(ip3)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www._jerry_.cl', 'qtype': '6'}]})
        data.set_expected('www._jerry_.cl', [
            {'server': 'encrypted(dnsip3)',
             'sender': 'encrypted(ip3)',
             'query': {
                 'qname': 'www._jerry_.cl', 'qtype': '6'}}])

        data.add_packet({'dest': 'encrypted(dnsip4)',
                         'source': 'encrypted(ip4)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www._pinky.cl', 'qtype': 'f'}]})
        data.set_expected('www._pinky.cl', [
            {'server': 'encrypted(dnsip4)',
             'sender': 'encrypted(ip4)',
             'query': {
                 'qname': 'www._pinky.cl', 'qtype': 'f'}}])

        # Normal data, critical qtypes
        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.nic.cl', 'qtype': '1'}]})
        data.add_packet({'dest': 'encrypted(dnsip2)',
                         'source': 'encrypted(ip2)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.niclabs.cl', 'qtype': '2'}]})
        data.add_packet({'dest': 'encrypted(dnsip3)',
                         'source': 'encrypted(ip3)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.jerry.cl', 'qtype': '6'}]})
        data.add_packet({'dest': 'encrypted(dnsip4)',
                         'source': 'encrypted(ip4)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.pinky.cl', 'qtype': 'f'}]})

        # Normal data
        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.nic.cl', 'qtype': '3'}]})
        data.add_packet({'dest': 'encrypted(dnsip2)',
                         'source': 'encrypted(ip2)',
                         'flags': '8000',
                         'queries': [
                             {'qname': 'www.niclabs.cl', 'qtype': '4'}]})
        data.add_packet({'dest': 'encrypted(dnsip3)',
                         'source': 'encrypted(ip3)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.jerry.cl', 'qtype': '5'}]})
        data.add_packet({'dest': 'encrypted(dnsip4)',
                         'source': 'encrypted(ip4)',
                         'flags': '8000',
                         'queries': [
                             {'qname': 'www.pinky.cl', 'qtype': '7'}]})

        # Underscore data, noncritical qtypes
        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.ni_c.cl', 'qtype': '3'}]})
        data.add_packet({'dest': 'encrypted(dnsip2)',
                         'source': 'encrypted(ip2)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.nic_labs.cl', 'qtype': '4'}]})
        data.add_packet({'dest': 'encrypted(dnsip3)',
                         'source': 'encrypted(ip3)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www._jerry_.cl', 'qtype': '5'}]})
        data.add_packet({'dest': 'encrypted(dnsip4)',
                         'source': 'encrypted(ip4)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www._pinky.cl', 'qtype': '7'}]})

        # Answers
        data.add_packet({'dest': 'encrypted(ip1)',
                         'source': 'encrypted(dnsip1)',
                         'flags': '8000',
                         'queries': [
                             {'qname': 'www.ni_c.cl', 'qtype': '1'}]})
        data.add_packet({'dest': 'encrypted(ip2)',
                         'source': 'encrypted(dnsip2)',
                         'flags': '8000',
                         'queries': [
                             {'qname': 'www.niclabs.cl', 'qtype': '2'}]})
        data.add_packet({'dest': 'encrypted(ip3)',
                         'source': 'encrypted(dnsip3)',
                         'flags': '8000',
                         'queries': [
                             {'qname': 'www.jerry.cl', 'qtype': '5'}]})
        data.add_packet({'dest': 'encrypted(ip4)',
                         'source': 'encrypted(dnsip4)',
                         'flags': '8000',
                         'queries': [
                             {'qname': 'www._pinky.cl', 'qtype': '7'}]})

        return data

    def data_different_case(self):
        data = PacketsExample()
        data.put_information('problematicQName', 'www.ni_c.cl')

        expected_list = []

        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'www.ni_c.cl', 'qtype': '1'}]})
        expected_list.append({'server': 'encrypted(dnsip1)',
                              'sender': 'encrypted(ip1)',
                              'query': {
                                  'qname': 'www.ni_c.cl', 'qtype': '1'}})

        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'WWW.NI_C.CL', 'qtype': '1'}]})
        expected_list.append({'server': 'encrypted(dnsip1)',
                              'sender': 'encrypted(ip1)',
                              'query': {
                                  'qname': 'WWW.NI_C.CL', 'qtype': '1'}})

        data.set_expected('www.ni_c.cl', expected_list)

        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'wwww.ni_c.cl', 'qtype': '1'}]})
        data.add_packet({'dest': 'encrypted(dnsip1)',
                         'source': 'encrypted(ip1)',
                         'flags': '0',
                         'queries': [
                             {'qname': 'WWW:NI_C.CL', 'qtype': '1'}]})

        return data

    def data_repeat_error(self):
        data = PacketsExample()
        data.put_information('problematicQNames', {
            'www.ni_c.cl', 'www.nic_labs.cl'})

        expected_list = []
        for i in range(3):
            data.add_packet({'dest': 'encrypted(dnsip1)',
                             'source': 'encrypted(ip1)',
                             'flags': '0',
                             'queries': [
                                 {'qname': 'www.ni_c.cl', 'qtype': '1'}]})
            expected_list.append({'server': 'encrypted(dnsip1)',
                                  'sender': 'encrypted(ip1)',
                                  'query': {
                                      'qname': 'www.ni_c.cl', 'qtype': '1'}})
        data.set_expected('www.ni_c.cl', expected_list)

        expected_list = []
        for i in range(2):
            data.add_packet({'dest': 'encrypted(dnsip2)',
                             'source': 'encrypted(ip2)',
                             'flags': '0',
                             'queries': [
                                 {'qname': 'www.nic_labs.cl', 'qtype': '2'}]})
            expected_list.append({'server': 'encrypted(dnsip2)',
                                  'sender': 'encrypted(ip2)',
                                  'query': {
                                      'qname': 'www.nic_labs.cl',
                                      'qtype': '2'}})
        data.set_expected('www.nic_labs.cl', expected_list)

        return data

    def setUp(self):
        self.reinit()

    def test_right_format(self):
        self.reinit()

        self.__p1(Packet({'dest': 'encrypted(dnsip1)',
                          'source': 'encrypted(ip1)',
                          'flags': '0',
                          'queries': [
                              {'qname': 'www.ni_c.cl', 'qtype': '1'}]}))
        result = self.__p1.get_data()

        self.assertEquals(type(result), dict)

        result_for_qname = result['www.ni_c.cl']
        self.assertEquals(type(result_for_qname), list)

        some_query = result_for_qname[0]
        self.assertEquals(type(some_query), dict)

        self.assertTrue('query' in some_query)
        self.assertTrue('sender' in some_query)
        self.assertTrue('server' in some_query)

        query_itself = some_query['query']

        self.assertTrue('qtype' in query_itself)
        self.assertTrue('qname' in query_itself)

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
        expected_problematic = example.get_information('problematicQNames')

        for source in result.keys():
            self.assertTrue(source in expected_problematic)

        for source in expected_problematic:
            self.assertTrue(source in result)
            self.assertEquals(example.expected_value(source), result[source])

    def test_data_different_case(self):
        self.reinit()

        example = self.data_different_case()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        expected_problematic = example.get_information('problematicQName')

        self.assertTrue(expected_problematic in result)
        self.assertItemsEqual(example.expected_value(
            expected_problematic), result[expected_problematic])

    def test_data_repeat_error(self):
        self.reinit()

        example = self.data_repeat_error()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        expected_problematic = example.get_information('problematicQNames')

        for source in expected_problematic:
            self.assertTrue(source in result)
            self.assertEquals(example.expected_value(source), result[source])

    def test_reset(self):
        self.reinit()

        example = self.data_example()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()
            expected_problematic = example.get_information('problematicQNames')

            for source in result.keys():
                self.assertTrue(source in expected_problematic)

            for source in expected_problematic:
                self.assertTrue(source in result)
                self.assertEquals(
                    example.expected_value(source), result[source])

            self.__p1.reset()

    def test_file(self):
        self.reinit()

        self.assertEquals(self.__stringbuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
