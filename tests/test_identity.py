import unittest
import StringIO

from packetsexample import PacketsExample
from prers.identity import Identity


class TestIdentity(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__stringbuffer2 = StringIO.StringIO()
        self.__p1 = Identity(self.__stringbuffer1)
        self.__p2 = Identity(self.__stringbuffer2)

    def data_example(self):
        data = PacketsExample()
        data.do_not_change_order()

        list_of_packets = []

        for i in range(5):
            data.add_packet({'flags': '8000', 'queries': [
                {'qname': 'www.nic.cl'}]})
            list_of_packets.append(
                {'flags': '8000', 'queries': [{'qname': 'www.nic.cl'}]})

        for i in range(4):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.niclabs.cl'}]})
            list_of_packets.append(
                {'flags': '0', 'queries': [{'qname': 'www.niclabs.cl'}]})

        for i in range(3):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.uchile.cl'}]})
            list_of_packets.append(
                {'flags': '0', 'queries': [{'qname': 'www.uchile.cl'}]})

        for i in range(3):
            data.add_packet({'flags': '8000', 'queries': [
                {'qname': 'www.jerry.cl'}]})
            list_of_packets.append(
                {'flags': '8000', 'queries': [{'qname': 'www.jerry.cl'}]})

        for i in range(2):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.pinky.cl'}]})
            list_of_packets.append(
                {'flags': '0', 'queries': [{'qname': 'www.pinky.cl'}]})

        data.put_information('packets', list_of_packets)

        return data

    def setUp(self):
        self.reinit()

    def test_right_format(self):
        self.reinit()

        result = self.__p1.get_data()

        self.assertEquals(type(result), list)

    def test_no_data(self):
        self.reinit()

        result = self.__p1.get_data()

        self.assertEquals([], result)

    def test_same_behavior(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)
        for packet in example:
            self.__p2(packet)

        result1 = self.__p1.get_data()
        result2 = self.__p2.get_data()

        self.assertListEqual(result1, result2)

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertListEqual(result, example.get_information('packets'))

    def test_reset(self):
        self.reinit()

        example = self.data_example()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            self.assertListEqual(result, example.get_information('packets'))

            self.__p1.reset()

    def test_file(self):
        self.reinit()

        self.assertEquals(self.__stringbuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
