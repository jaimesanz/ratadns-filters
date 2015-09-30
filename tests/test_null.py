__author__ = 'sking32'

import unittest
import StringIO

from packetsexample import PacketsExample
from prers.null import NullPreR


class TestNullPreR(unittest.TestCase):

    def reInit(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = NullPreR(self.__stringBuffer1)
        self.__p2 = NullPreR(self.__stringBuffer2)

    def dataExample(self):
        data = PacketsExample()
        data.addPacket({'flags' : '0', 'id' : '12cb'})
        data.addPacket({'flags' : '8000', 'id' : '12cb'})

        return data

    def setUp(self):
        self.reInit()


    def test_rightFormatNoData(self):
        self.reInit()

        result = self.__p1.get_data()

        self.assertEquals(result, None)

    def test_sameBehavior(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)
            self.__p2(packet)

        result1 = self.__p1.get_data()
        result2 = self.__p2.get_data()

        self.assertEquals(result1, result2)

    def test_dataExample(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(result, None)

    def test_reset(self):
        self.reInit()

        example = self.dataExample()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            self.assertEquals(result, None)

            self.__p1.reset()

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
