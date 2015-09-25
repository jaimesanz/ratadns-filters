__author__ = 'sking32'

import unittest
import StringIO
import operator

from packetsexample import PacketsExample
from prers.topn import TopN


class TestTopN(unittest.TestCase):

    def reInit(self, n1=3, n2=3):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = TopN(self.__stringBuffer1, n1)
        self.__p2 = TopN(self.__stringBuffer2, n2)

    def dataExample(self):

        queries = {'www.nic.cl' : 5, 'www.niclabs.cl' : 4, 'www.uchile.cl' : 3, 'www.jerry.cl' : 3, 'www.pinky.cl' : 2}
        data = PacketsExample(queries)
        data.putInformation('sortedQnames', sorted(queries.items(), key=operator.itemgetter(1), reverse=True)) #Returns a list with the elements of the dict in descending order of its keys

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
        queries = {'www.nic.cl' : 5, 'www.niclabs.cl' : 10}
        data = PacketsExample(queries)
        data.putInformation('sortedQnames', sorted(queries.items(), key=operator.itemgetter(1), reverse=True)) #Returns a list with the elements of the dict in descending order of its keys

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

    def test_numberOfQnames(self):
        example = self.dataExample()
        tops = example.getInformation('sortedQnames')

        for n in range(2*len(tops)):
            self.reInit(n)
            n = min(n, len(tops))

            for packet in example:
                self.__p1(packet)
            result = self.__p1.get_data()
            self.assertEquals(n, len(result))

    def test_subset(self):
        n = 3
        self.reInit(n)

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)

        subdictResult = self.__p1.get_data()

        self.reInit(n+1)
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        self.assertTrue(set(subdictResult.items()).issubset(set(result.items())))
        self.assertFalse(set(result.items()).issubset(set(subdictResult.items())))


    def test_equalRating(self):
        n = 3
        self.reInit(n)

        example = self.dataEqualRating()
        for packet in example:
            self.__p1(packet)

        self.assertEquals(len(self.__p1.get_data()), example.getInformation('equalQnames'))

    def test_dataExample(self):
        n = 3
        self.reInit(n)

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(n, len(result))
        tops = example.getInformation('sortedQnames')
        for i in range(n):
            qname = tops[i][0]
            self.assertTrue(result.has_key(qname))
            self.assertEquals(example.expectedValue(qname) ,result[qname])

    def test_dataDifferentCase(self):
        n = 3
        self.reInit(n)

        example = self.dataDifferentCase()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(n, len(result))
        tops = example.getInformation('sortedQnames')
        for i in range(n):
            qname = tops[i][0]
            self.assertTrue(result.has_key(qname))
            self.assertEquals(example.expectedValue(qname) ,result[qname])

    def test_reset(self):
        n = 3
        self.reInit(n)

        for i in range(2):
            example = self.dataExample()
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            self.assertEquals(n, len(result))
            tops = example.getInformation('sortedQnames')
            for i in range(n):
                qname = tops[i][0]
                self.assertTrue(result.has_key(qname))
                self.assertEquals(example.expectedValue(qname) ,result[qname])
            self.__p1.reset()

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
