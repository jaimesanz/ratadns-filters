__author__ = 'sking32'

import unittest
import StringIO

from packetsexample import PacketsExample
from prers.onlyqueries import OnlyQueries


class TestOnlyQueries(unittest.TestCase):

    def reInit(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = OnlyQueries(self.__stringBuffer1)
        self.__p2 = OnlyQueries(self.__stringBuffer2)

    def dataExample(self):
        data = PacketsExample()
        data.doNotChangeOrder()

        listOfQueries = []

        for i in range(5) :
            data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.nic.cl'}]})

        for i in range(4) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.niclabs.cl'}]})
            listOfQueries.append({'flags': '0', 'queries' : [{'qname' : 'www.niclabs.cl'}]})

        for i in range(3) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.uchile.cl'}]})
            listOfQueries.append({'flags': '0', 'queries' : [{'qname' : 'www.uchile.cl'}]})

        for i in range(3) :
            data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.jerry.cl'}]})

        for i in range(2) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.pinky.cl'}]})
            listOfQueries.append({'flags': '0', 'queries' : [{'qname' : 'www.pinky.cl'}]})

        data.putInformation('queries', listOfQueries)

        return data

    def dataOnlyAnswers(self):
        data = PacketsExample()
        data.doNotChangeOrder()

        for i in range(5) :
            data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.nic.cl'}]})

        for i in range(3) :
            data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.jerry.cl'}]})

        for i in range(2) :
            data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.pinky.cl'}]})

        return data

    def setUp(self):
        self.reInit()


    def test_rightFormat(self):
        self.reInit()

        result = self.__p1.get_data()

        self.assertEquals(type(result), list)

    def test_noData(self):
        self.reInit()

        result = self.__p1.get_data()

        self.assertEquals([], result)

    def test_sameBehavior(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)
            self.__p2(packet)

        result1 = self.__p1.get_data()
        result2 = self.__p2.get_data()

        self.assertListEqual(result1, result2)

    def test_dataExample(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertListEqual(result, example.getInformation('queries'))

    def test_dataOnlyAnswers(self):
        self.reInit()

        example = self.dataOnlyAnswers()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertListEqual(result, [])

    def test_reset(self):
        self.reInit()

        example = self.dataExample()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            self.assertListEqual(result, example.getInformation('queries'))

            self.__p1.reset()

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
