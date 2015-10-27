import unittest
import StringIO
from time import time

from packetsexample import PacketsExample
from prers.pqaps import PacketsQueriesAndAnswersPerSecond


class TestPacketsQueriesAndAnswersPerSecond(unittest.TestCase):

    def reInit(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = PacketsQueriesAndAnswersPerSecond(self.__stringBuffer1)
        self.__p2 = PacketsQueriesAndAnswersPerSecond(self.__stringBuffer2)

    def dataExample(self):
        na = 2
        nq = 2
        data = PacketsExample({'na': na, 'nq': nq})

        for i in range(na):
            data.addPacket({'flags': '8000'})
        for i in range(nq):
            data.addPacket({'flags': '0'})

        return data

    def dataOnlyQueries(self):
        na = 0
        nq = 2
        data = PacketsExample({'na': na, 'nq': nq})

        data = PacketsExample()
        for i in range(nq):
            data.addPacket({'flags': '0'})

        return data

    def dataOnlyAnswers(self):
        na = 2
        nq = 0
        data = PacketsExample({'na': na, 'nq': nq})

        for i in range(na):
            data.addPacket({'flags': '8000'})

        return data

    def setUp(self):
        self.reInit()

    def test_rightFormat(self):
        self.reInit()

        result = self.__p1.get_data()

        self.assertEquals(type(result), dict)

        self.assertTrue('pps' in result)
        self.assertEqual(type(result['pps']), float)
        self.assertGreaterEqual(result['pps'], 0)

        self.assertTrue('qps' in result)
        self.assertEqual(type(result['qps']), float)
        self.assertGreaterEqual(result['qps'], 0)

        self.assertTrue('aps' in result)
        self.assertEqual(type(result['aps']), float)
        self.assertGreaterEqual(result['aps'], 0)

    def test_noData(self):
        self.reInit()

        result = self.__p1.get_data()

        self.assertEqual(result['pps'], 0)
        self.assertEqual(result['qps'], 0)
        self.assertEqual(result['aps'], 0)

    def test_dataExample(self):  # AQUI VOY

        beforeInitTime = time()
        self.reInit()
        afterInitTime = time()

        example = self.dataExample()

        for packet in example:
            self.__p1(packet)

        beforeEndTime = time()
        result = self.__p1.get_data()
        afterEndTime = time()

        na = example.expectedValue('na')
        nq = example.expectedValue('nq')
        self.assertLessEqual((na+nq) / (afterEndTime - beforeInitTime),
                             result['pps'])
        self.assertGreaterEqual((na+nq) / (beforeEndTime - afterInitTime),
                                result['pps'])

        self.assertLessEqual(nq / (afterEndTime - beforeInitTime),
                             result['qps'])
        self.assertGreaterEqual(nq / (beforeEndTime - afterInitTime),
                                result['qps'])

        self.assertLessEqual(na / (afterEndTime - beforeInitTime),
                             result['aps'])
        self.assertGreaterEqual(na / (beforeEndTime - afterInitTime),
                                result['aps'])

    def test_dataOnlyQueries(self):

        self.reInit()

        example = self.dataOnlyQueries()

        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertLessEqual(result['aps'], 0)

    def test_dataOnlyAnswers(self):

        self.reInit()

        example = self.dataOnlyAnswers()

        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertLessEqual(result['qps'], 0)

    def test_reset(self):
        beforeInitTime = time()
        self.reInit()
        afterInitTime = time()

        example = self.dataExample()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            beforeEndTime = time()
            result = self.__p1.get_data()
            afterEndTime = time()

            na = example.expectedValue('na')
            nq = example.expectedValue('nq')
            self.assertLessEqual((na+nq) / (afterEndTime - beforeInitTime),
                                 result['pps'])
            self.assertGreaterEqual((na+nq) / (beforeEndTime - afterInitTime),
                                    result['pps'])

            self.assertLessEqual(example.expectedValue(
                'nq') / (afterEndTime - beforeInitTime), result['qps'])
            self.assertGreaterEqual(example.expectedValue(
                'nq') / (beforeEndTime - afterInitTime), result['qps'])

            self.assertLessEqual(example.expectedValue(
                'na') / (afterEndTime - beforeInitTime), result['aps'])
            self.assertGreaterEqual(example.expectedValue(
                'na') / (beforeEndTime - afterInitTime), result['aps'])

            beforeInitTime = time()
            self.__p1.reset()
            afterInitTime = time()

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
