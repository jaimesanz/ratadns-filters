
import unittest
import StringIO

from packetsexample import PacketsExample
from prers.qnamecounter import QueriesNameCounter


class TestIssue27(unittest.TestCase):

    def reInit(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = QueriesNameCounter(self.__stringBuffer1)
        self.__p2 = QueriesNameCounter(self.__stringBuffer2)

    def dataExample(self):
        data = PacketsExample()
        data.addPacket({'flags': '0', 'queries': []})

        data.setExpected('', 1)

        data.putInformation('QNames', {''})
        return data

    def setUp(self):
        self.reInit()

    def test_rightFormat(self):
        self.reInit()

        example = self.dataExample()

        for packet in example:
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

        for qname in result1.keys():
            self.assertTrue(qname in result2)
            self.assertEquals(result1[qname], result2[qname])

        for qname in result2.keys():
            self.assertTrue(qname in result1)

    def test_dataExample(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for qname in example.getInformation('QNames'):
            self.assertTrue(qname in result)
            self.assertEquals(example.expectedValue(qname), result[qname])

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
