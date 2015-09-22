__author__ = 'sking32'

import unittest
import StringIO

from packetsexample import PacketsExample
from prers.identity import Identity


class TestIdentity(unittest.TestCase):

    def reInit(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = Identity(self.__stringBuffer1)
        self.__p2 = Identity(self.__stringBuffer2)

    def dataExample(self):
        data = PacketsExample()
        data.doNotChangeOrder()

        listOfPackets = []

        for i in range(5) :
            data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.nic.cl'}]})
            listOfPackets.append({'flags': '8000', 'queries' : [{'qname' : 'www.nic.cl'}]})

        for i in range(4) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.niclabs.cl'}]})
            listOfPackets.append({'flags': '0', 'queries' : [{'qname' : 'www.niclabs.cl'}]})

        for i in range(3) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.uchile.cl'}]})
            listOfPackets.append({'flags': '0', 'queries' : [{'qname' : 'www.uchile.cl'}]})

        for i in range(3) :
            data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.jerry.cl'}]})
            listOfPackets.append({'flags': '8000', 'queries' : [{'qname' : 'www.jerry.cl'}]})

        for i in range(2) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.pinky.cl'}]})
            listOfPackets.append({'flags': '0', 'queries' : [{'qname' : 'www.pinky.cl'}]})

        data.putInformation('packets', listOfPackets)

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

        self.assertListEqual(result, example.getInformation('packets'))

    def test_reset(self):
        self.reInit()

        example = self.dataExample()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            self.assertListEqual(result, example.getInformation('packets'))

            self.__p1.reset()

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
