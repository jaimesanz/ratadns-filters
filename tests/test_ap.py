__author__ = 'sking32'

import unittest
import StringIO

from prers.ap import AlonePackets


class TestAlonePackets(unittest.TestCase):

    def reInit(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = AlonePackets(self.__stringBuffer1)
        self.__p2 = AlonePackets(self.__stringBuffer2)

    def dataExample(self):
        data = []
        data.append({'flags' : '8000', 'id' : '1111'}) #Answer without query
        data.append({'flags' : '0', 'id' : '12cb'})
        data.append({'flags' : '8000', 'id' : '12cb'})
        data.append({'flags' : '0', 'id' : '3333'}) #Query without answer
        return data

    def setUp(self):
        self.reInit()


    def test_rightFormat(self):
        self.reInit()

        result = self.__p1.get_data()

        self.assertTrue(type(result) == dict)
        self.assertTrue(result.has_key('queries'))
        self.assertTrue(result.has_key('answers'))
        self.assertTrue(result.has_key('AloneAnswers'))
        self.assertTrue(result.has_key('AloneQueries'))

    def test_noData(self):
        self.reInit()

        result = self.__p1.get_data()

        self.assertEquals(0, result['queries'])
        self.assertEquals(0, result['answers'])
        self.assertEquals([], result['AloneAnswers'])
        self.assertEquals([], result['AloneQueries'])

    def test_sameBehavior(self):
        self.reInit()
        for packet in self.dataExample():
            self.__p1(packet)
            self.__p2(packet)

        result1 = self.__p1.get_data()
        result2 = self.__p2.get_data()

        self.assertEquals(result1['queries'], result2['queries'])
        self.assertEquals(result1['answers'], result2['answers'])
        self.assertEquals(sorted(result1['AloneAnswers']), sorted(result2['AloneAnswers']))
        self.assertEquals(sorted(result1['AloneQueries']), sorted(result2['AloneQueries']))

    def test_dataExample(self):
        self.reInit()
        for packet in self.dataExample():
            self.__p1(packet)

        result = self.__p1.get_data()

        #Defininir tipo de dato para que esto este harcodeado en solo una parte
        self.assertEquals(2 ,result['queries'])
        self.assertEquals(2, result['answers'])
        self.assertEquals(sorted([{'flags' : '8000', 'id' : '1111'}]), sorted(result['AloneAnswers']))
        self.assertEquals(sorted([{'flags' : '0', 'id' : '3333'}]), sorted(result['AloneQueries']))

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
