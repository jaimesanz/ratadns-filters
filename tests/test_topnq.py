__author__ = 'sking32'

import unittest
import StringIO

from packetsexample import PacketsExample
from prers.topnq import TopNQ


class TestTopNQ(unittest.TestCase):

    def reInit(self, n1=3, n2=3):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = TopNQ(self.__stringBuffer1, n1)
        self.__p2 = TopNQ(self.__stringBuffer2, n2)

    def dataExample(self):

        data = PacketsExample({'www.nic.cl' : 5, 'www.niclabs.cl' : 4, 'www.uchile.cl' : 3, 'www.jerry.cl' : 3, 'www.pinky.cl' : 2})

        for i in range(5) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.nic.cl'}]})

        for i in range(4) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.niclabs.cl'}]})

        for i in range(3) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.uchile.cl'}]})

        for i in range(3) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.jerry.cl'}]})

        for i in range(2) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.pinky.cl'}]})

        data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.nic.cl'}]})#Answers
        data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.brain.cl'}]})
        data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.pinky.cl'}]})

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

        self.assertDictEqual({}, result)

    def test_dataJustAnswers(self):
        pass

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

    def test_subset(self):
        pass

    def test_equalRating(self):
        pass

    def test_lessThanN(self):
        pass

    def test_dataExample(self):
        pass


    def test_reset(self):
        pass

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
