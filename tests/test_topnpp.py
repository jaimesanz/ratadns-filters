__author__ = 'sking32'

import unittest
import StringIO
import operator

from packetsexample import PacketsExample
from prers.topnpp import TopNPP


class TestTopNPP(unittest.TestCase):

    def reInit(self, n1=3, n2=3):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = TopNPP(self.__stringBuffer1, n=n1)
        self.__p2 = TopNPP(self.__stringBuffer2, n=n2)

    def dataExample(self):

        queries = {'www.nic.cl' : 5, 'www.niclabs.cl' : 4, 'www.uchile.cl' : 3, 'www.jerry.cl' : 3, 'www.pinky.cl' : 2}
        data = PacketsExample(queries)
        data.putInformation('sortedQnames', map(list, sorted(queries.items(), key=operator.itemgetter(1), reverse=True))) #Returns a list with the elements of the dict in descending order of its keys

        for i in range(5) :
            data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.nic.cl'}]})

        for i in range(4) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.niclabs.cl'}]})

        for i in range(3) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.uchile.cl'}]})

        for i in range(3) :
            data.addPacket({'flags': '8000', 'queries' : [{'qname' : 'www.jerry.cl'}]})

        for i in range(2) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.pinky.cl'}]})

        return data

    def dataDifferentCase(self):
        queries = {'www.nic.cl' : 10, 'www.niclabs.cl' : 5, 'wwww.niclabs.cl' : 6}
        data = PacketsExample(queries)
        data.putInformation('sortedQnames', map(list, sorted(queries.items(), key=operator.itemgetter(1), reverse=True))) #Returns a list with the elements of the dict in descending order of its keys

        for i in range(5) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.nic.cl'}]})
        for i in range(5) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'WWW.NIC.CL'}]})

        for i in range(5) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.niclabs.cl'}]})
        for i in range(6) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'WwWW.NicLaBs.cl'}]})

        return data

    def dataEqualRating(self):
        n = 10
        queries = {'www.nic.cl' : n, 'www.niclabs.cl' : n, 'www.uchile.cl' : n, 'www.jerry.cl' : n, 'www.pinky.cl' : n}
        data = PacketsExample(queries)
        data.putInformation('equalQnames', 5)
        for i in range(n) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.nic.cl'}]})

        for i in range(n) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.niclabs.cl'}]})

        for i in range(n) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.uchile.cl'}]})

        for i in range(n) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.jerry.cl'}]})

        for i in range(n) :
            data.addPacket({'flags': '0', 'queries' : [{'qname' : 'www.pinky.cl'}]})

        return data

    def setUp(self):
        self.reInit()

    def test_rightFormat(self):
        n = 3
        self.reInit(3)

        example = self.dataExample()

        for packet in example :
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(type(result), list)
        self.assertGreaterEqual(len(result), n) #Not always(when there is not enough info)

        for p in result:
            self.assertEquals(type(p), list)
            self.assertEquals(len(p), 2)
            self.assertEquals(type(p[0]), str)
            self.assertEquals(type(p[1]), int)


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

        self.assertItemsEqual(result1, result2)


    def test_numberOfQnames(self):
        example = self.dataExample()
        tops = example.getInformation('sortedQnames')

        for n in range(2*len(tops)):
            self.reInit(n)
            n = min(n, len(tops))

            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()
            self.assertGreaterEqual(len(result), n)

    def test_subset(self):
        n = 3
        self.reInit(n)

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)

        subResult = self.__p1.get_data()

        self.reInit(n+2)
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()


        for p in subResult:
            self.assertTrue(p in result)

        existeDiferente = False
        for p in result:
            existeDiferente = existeDiferente or not(p in subResult)
        self.assertTrue(existeDiferente)

    def test_equalRating(self):
        n = 3
        self.reInit(n)

        example = self.dataEqualRating()
        for packet in example:
            self.__p1(packet)

        self.assertEquals(len(self.__p1.get_data()), example.getInformation('equalQnames'))

    def test_dataExample(self):
        n = 4
        self.reInit(n)

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertGreaterEqual(len(result), n)
        tops = example.getInformation('sortedQnames')

        for i in range(len(result)-1):
            self.assertGreaterEqual(result[i][1], result[i+1][1])
        self.assertItemsEqual(tops[0:len(result)], result)

    def test_dataDifferentCase(self):
        n = 3
        self.reInit(n)

        example = self.dataDifferentCase()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        self.assertGreaterEqual(len(result), n)
        tops = example.getInformation('sortedQnames')
        self.assertItemsEqual(tops[0:len(result)], result)

    def test_reset(self):
        n = 4
        self.reInit(n)

        for i in range(2):
            example = self.dataExample()
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            self.assertGreaterEqual(len(result), n)
            tops = example.getInformation('sortedQnames')
            self.assertItemsEqual(tops[0:len(result)], result)
            self.__p1.reset()

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
