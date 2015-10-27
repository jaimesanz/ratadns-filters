import unittest
import StringIO

from packetsexample import PacketsExample
from prers.ap import AlonePackets


class TestAlonePackets(unittest.TestCase):

    def reInit(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = AlonePackets(self.__stringBuffer1)
        self.__p2 = AlonePackets(self.__stringBuffer2)

    def dataExample(self):
        data = PacketsExample({'queries': 2, 'answers': 2})
        answerWithoutQuery = {'flags': '8000', 'id': '1111'}
        queryWithoutAnswer = {'flags': '0', 'id': '3333'}

        data.addPacket(answerWithoutQuery)  # Answer without query
        data.addPacket({'flags': '0', 'id': '12cb'})
        data.addPacket({'flags': '8000', 'id': '12cb'})
        data.addPacket(queryWithoutAnswer)  # Query without answer

        data.setExpected('AloneAnswers', [answerWithoutQuery])
        data.setExpected('AloneQueries', [queryWithoutAnswer])

        return data

    def dataWithoutQueries(self):
        answers = [{'flags': '8000', 'id': 'a6c7'}, {
            'flags': '8000', 'id': '5433'}, {'flags': '8000', 'id': 'a276'}]
        data = PacketsExample({'queries': 0, 'answers': len(answers)})

        for answer in answers:
            data.addPacket(answer)

        data.setExpected('AloneAnswers', answers)
        data.setExpected('AloneQueries', [])

        return data

    def dataWithoutAnswers(self):
        queries = [{'flags': '0', 'id': 'a6c7'}, {'flags': '0', 'id': '5433'},
                   {'flags': '0', 'id': 'a276'}, {'flags': '0', 'id': '4321'}]
        data = PacketsExample({'queries': len(queries), 'answers': 0})

        for query in queries:
            data.addPacket(query)

        data.setExpected('AloneAnswers', [])
        data.setExpected('AloneQueries', queries)

        return data

    def dataWithoutAlonePackets(self):
        data = PacketsExample({'queries': 2, 'answers': 2})

        data.addPacket({'flags': '8000', 'id': '1111'})
        data.addPacket({'flags': '0', 'id': '12cb'})
        data.addPacket({'flags': '8000', 'id': '12cb'})
        data.addPacket({'flags': '0', 'id': '1111'})

        data.setExpected('AloneAnswers', [])
        data.setExpected('AloneQueries', [])

        return data

    def setUp(self):
        self.reInit()

    def test_rightFormat(self):
        self.reInit()

        result = self.__p1.get_data()

        self.assertEquals(type(result), dict)
        self.assertTrue('queries' in result)
        self.assertTrue('answers' in result)
        self.assertTrue('AloneAnswers' in result)
        self.assertTrue('AloneQueries' in result)

        self.assertEquals(type(result['AloneAnswers']), list)
        self.assertEquals(type(result['AloneQueries']), list)

    def test_noData(self):
        self.reInit()

        result = self.__p1.get_data()

        self.assertEquals(0, result['queries'])
        self.assertEquals(0, result['answers'])
        self.assertEquals([], result['AloneAnswers'])
        self.assertEquals([], result['AloneQueries'])

    def test_sameBehavior(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)
            self.__p2(packet)

        result1 = self.__p1.get_data()
        result2 = self.__p2.get_data()

        self.assertEquals(result1['queries'], result2['queries'])
        self.assertEquals(result1['answers'], result2['answers'])
        self.assertItemsEqual(result1['AloneAnswers'], result2['AloneAnswers'])
        self.assertItemsEqual(result1['AloneQueries'], result2['AloneQueries'])

    def test_dataExample(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(example.expectedValue('queries'), result['queries'])
        self.assertEquals(example.expectedValue('answers'), result['answers'])
        self.assertItemsEqual(example.expectedValue(
            'AloneAnswers'), result['AloneAnswers'])
        self.assertItemsEqual(example.expectedValue(
            'AloneQueries'), result['AloneQueries'])

    def test_reset(self):
        self.reInit()

        example = self.dataExample()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            self.assertEquals(example.expectedValue(
                'queries'), result['queries'])
            self.assertEquals(example.expectedValue(
                'answers'), result['answers'])
            self.assertItemsEqual(example.expectedValue(
                'AloneAnswers'), result['AloneAnswers'])
            self.assertItemsEqual(example.expectedValue(
                'AloneQueries'), result['AloneQueries'])

            self.__p1.reset()

    def test_dataWithoutQueries(self):
        self.reInit()

        example = self.dataWithoutQueries()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(example.expectedValue('queries'), result['queries'])
        self.assertEquals(example.expectedValue('answers'), result['answers'])
        self.assertItemsEqual(example.expectedValue(
            'AloneAnswers'), result['AloneAnswers'])
        self.assertItemsEqual(example.expectedValue(
            'AloneQueries'), result['AloneQueries'])

    def test_dataWithoutAnswers(self):
        self.reInit()

        example = self.dataWithoutAnswers()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(example.expectedValue('queries'), result['queries'])
        self.assertEquals(example.expectedValue('answers'), result['answers'])
        self.assertItemsEqual(example.expectedValue(
            'AloneAnswers'), result['AloneAnswers'])
        self.assertItemsEqual(example.expectedValue(
            'AloneQueries'), result['AloneQueries'])

    def test_dataWithoutAlonePackets(self):
        self.reInit()

        example = self.dataWithoutAlonePackets()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(example.expectedValue('queries'), result['queries'])
        self.assertEquals(example.expectedValue('answers'), result['answers'])
        self.assertItemsEqual(example.expectedValue(
            'AloneAnswers'), result['AloneAnswers'])
        self.assertItemsEqual(example.expectedValue(
            'AloneQueries'), result['AloneQueries'])

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
