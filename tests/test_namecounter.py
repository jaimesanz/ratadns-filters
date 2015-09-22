__author__ = 'sking32'

import unittest
import StringIO

from packetsexample import PacketsExample
from prers.namecounter import NameCounter


class TestNameCounter(unittest.TestCase):

    def reInit(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = NameCounter(self.__stringBuffer1)
        self.__p2 = NameCounter(self.__stringBuffer2)

    def dataExample(self):
        data = PacketsExample()

        for i in range(5) :
            data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.nic.cl'}]})
        data.setExpected('www.nic.cl', 5)

        for i in range(4) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.niclabs.cl'}]})
        data.setExpected('www.niclabs.cl', 4)

        for i in range(3) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.uchile.cl'}]})
        data.setExpected('www.uchile.cl', 3)

        for i in range(3) :
            data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.jerry.cl'}]})
        data.setExpected('www.jerry.cl', 3)

        for i in range(2) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.pinky.cl'}]})
        data.setExpected('www.pinky.cl', 2)

        return data

        return data

    def setUp(self):
        self.reInit()

    def test_rightFormat(self):
        self.reInit()

        example = self.dataExample()

        for packet in example :
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertTrue(type(result) == dict)
        for key in result.keys():
            self.assertTrue(type(key) == str)
            self.assertTrue(type(result[key]) == int)

            frec = result[key]
            self.assertGreater(frec, 0)

    def test_noData(self):
        self.reInit()

        result = self.__p1.get_data()

        self.assertEquals({}, result)

    def test_sameBehavior(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)
            self.__p2(packet)

        result1 = self.__p1.get_data()
        result2 = self.__p2.get_data()

        for qname in result1.keys() :
            self.assertTrue(result2.has_key(qname))
            self.assertEquals(result1[qname], result2[qname])

        for qname in result2.keys() :
            self.assertTrue(result1.has_key(qname))


    def test_dataExample(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qname in result.keys():
            self.assertEquals(example.expectedValue(qname) ,result[qname])


    def test_reset(self):
        self.reInit()

        example = self.dataExample()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            for qname in result.keys():
                self.assertEquals(example.expectedValue(qname) ,result[qname])

            self.__p1.reset()

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
