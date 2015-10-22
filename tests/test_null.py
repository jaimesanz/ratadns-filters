import unittest
import StringIO

from packetsexample import PacketsExample
from prers.null import NullPreR


class TestNullPreR(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__stringbuffer2 = StringIO.StringIO()
        self.__p1 = NullPreR(self.__stringbuffer1)
        self.__p2 = NullPreR(self.__stringbuffer2)

    def data_example(self):
        data = PacketsExample()
        data.add_packet({'flags': '0', 'id': '12cb'})
        data.add_packet({'flags': '8000', 'id': '12cb'})

        return data

    def setUp(self):
        self.reinit()

    def test_right_format_no_data(self):
        self.reinit()

        result = self.__p1.get_data()

        self.assertEquals(result, None)

    def test_same_behavior(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)
            self.__p2(packet)

        result1 = self.__p1.get_data()
        result2 = self.__p2.get_data()

        self.assertEquals(result1, result2)

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(result, None)

    def test_reset(self):
        self.reinit()

        example = self.data_example()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            self.assertEquals(result, None)

            self.__p1.reset()

    def test_file(self):
        self.reinit()

        self.assertEquals(self.__stringbuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
