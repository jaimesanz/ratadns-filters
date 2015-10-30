import unittest
import StringIO

from packetsexample import PacketsExample
from prers.qnamecounter import QueriesNameCounter


class TestQueriesNameCounter(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__stringbuffer2 = StringIO.StringIO()
        self.__p1 = QueriesNameCounter(self.__stringbuffer1)
        self.__p2 = QueriesNameCounter(self.__stringbuffer2)

    def data_example(self):
        data = PacketsExample()

        for i in range(4):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.niclabs.cl'}]})
        data.set_expected('www.niclabs.cl', 4)

        for i in range(3):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.uchile.cl'}]})
        data.set_expected('www.uchile.cl', 3)

        for i in range(2):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.pinky.cl'}]})
        data.set_expected('www.pinky.cl', 2)

        data.put_information(
            'QNames', {'www.niclabs.cl', 'www.uchile.cl', 'www.pinky.cl'})
        return data

    def data_only_answers(self):

        data = PacketsExample()
        for i in range(5):
            data.add_packet({'flags': '8000', 'queries': [
                {'qname': 'www.nic.cl'}]})
        data.set_expected('www.nic.cl', 5)

        for i in range(3):
            data.add_packet({'flags': '8000', 'queries': [
                {'qname': 'www.jerry.cl'}]})
        data.set_expected('www.jerry.cl', 3)

        return data

    def data_differen_case(self):
        data = PacketsExample()

        for i in range(5):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.nic.cl'}]})
        for i in range(5):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'WWW.NIC.CL'}]})
        data.set_expected('www.nic.cl', 10)

        for i in range(5):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'WWW:NIC.CL'}]})
        for i in range(5):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'wwww.nic.cl'}]})
        data.put_information('criticalQName', 'www.nic.cl')
        return data

    def setUp(self):
        self.reinit()

    def test_right_format(self):
        self.reinit()

        example = self.data_example()

        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertTrue(type(result) == dict)
        for key in result.keys():
            self.assertTrue(type(key) == str)
            self.assertTrue(type(result[key]) == int)

            frec = result[key]
            self.assertGreater(frec, 0)

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

        for qname in result1.keys():
            self.assertTrue(qname in result2)
            self.assertEquals(result1[qname], result2[qname])

        for qname in result2.keys():
            self.assertTrue(qname in result1)

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qname in example.get_information('QNames'):
            self.assertTrue(qname in result)
            self.assertEquals(example.expected_value(qname), result[qname])

    def test_data_only_answers(self):
        self.reinit()

        example = self.data_only_answers()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        self.assertEquals(result, {})

    def test_data_different_case(self):
        self.reinit()

        example = self.data_differen_case()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        critical = example.get_information('criticalQName')
        self.assertEquals(example.expected_value(critical), result[critical])

    def test_reset(self):
        self.reinit()

        example = self.data_example()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            for qname in result.keys():
                self.assertEquals(example.expected_value(qname), result[qname])

            self.__p1.reset()

    def test_file(self):
        self.reinit()

        self.assertEquals(self.__stringbuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
