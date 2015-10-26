import unittest
import StringIO

from packetsexample import PacketsExample
from prers.ap import AlonePackets


class TestAlonePackets(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__stringbuffer2 = StringIO.StringIO()
        self.__p1 = AlonePackets(self.__stringbuffer1)
        self.__p2 = AlonePackets(self.__stringbuffer2)

    def data_example(self):
        data = PacketsExample({'queries': 2, 'answers': 2})
        answer_without_query = {'flags': '8000', 'id': '1111'}
        query_without_answer = {'flags': '0', 'id': '3333'}

        data.add_packet(answer_without_query)  # Answer without query
        data.add_packet({'flags': '0', 'id': '12cb'})
        data.add_packet({'flags': '8000', 'id': '12cb'})
        data.add_packet(query_without_answer)  # Query without answer

        data.set_expected('AloneAnswers', [answer_without_query])
        data.set_expected('AloneQueries', [query_without_answer])

        return data

    def data_without_queries(self):
        answers = [{'flags': '8000', 'id': 'a6c7'}, {
            'flags': '8000', 'id': '5433'}, {'flags': '8000', 'id': 'a276'}]
        data = PacketsExample({'queries': 0, 'answers': len(answers)})

        for answer in answers:
            data.add_packet(answer)

        data.set_expected('AloneAnswers', answers)
        data.set_expected('AloneQueries', [])

        return data

    def data_without_answers(self):
        queries = [{'flags': '0', 'id': 'a6c7'}, {'flags': '0', 'id': '5433'},
                   {'flags': '0', 'id': 'a276'}, {'flags': '0', 'id': '4321'}]
        data = PacketsExample({'queries': len(queries), 'answers': 0})

        for query in queries:
            data.add_packet(query)

        data.set_expected('AloneAnswers', [])
        data.set_expected('AloneQueries', queries)

        return data

    def data_without_alonePackets(self):
        data = PacketsExample({'queries': 2, 'answers': 2})

        data.add_packet({'flags': '8000', 'id': '1111'})
        data.add_packet({'flags': '0', 'id': '12cb'})
        data.add_packet({'flags': '8000', 'id': '12cb'})
        data.add_packet({'flags': '0', 'id': '1111'})

        data.set_expected('AloneAnswers', [])
        data.set_expected('AloneQueries', [])

        return data

    def setUp(self):
        self.reinit()

    def test_right_format(self):
        self.reinit()

        result = self.__p1.get_data()

        self.assertEquals(type(result), dict)
        self.assertTrue('queries' in result)
        self.assertTrue('answers' in result)
        self.assertTrue('AloneAnswers' in result)
        self.assertTrue('AloneQueries' in result)

        self.assertEquals(type(result['AloneAnswers']), list)
        self.assertEquals(type(result['AloneQueries']), list)

    def test_no_data(self):
        self.reinit()

        result = self.__p1.get_data()

        self.assertEquals(0, result['queries'])
        self.assertEquals(0, result['answers'])
        self.assertEquals([], result['AloneAnswers'])
        self.assertEquals([], result['AloneQueries'])

    def test_same_behavior(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)
        for packet in example:
            self.__p2(packet)

        result1 = self.__p1.get_data()
        result2 = self.__p2.get_data()

        self.assertEquals(result1['queries'], result2['queries'])
        self.assertEquals(result1['answers'], result2['answers'])
        self.assertItemsEqual(result1['AloneAnswers'], result2['AloneAnswers'])
        self.assertItemsEqual(result1['AloneQueries'], result2['AloneQueries'])

    def test_data_example(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(example.expected_value('queries'), result['queries'])
        self.assertEquals(example.expected_value('answers'), result['answers'])
        self.assertItemsEqual(example.expected_value(
            'AloneAnswers'), result['AloneAnswers'])
        self.assertItemsEqual(example.expected_value(
            'AloneQueries'), result['AloneQueries'])

    def test_reset(self):
        self.reinit()

        example = self.data_example()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            self.assertEquals(example.expected_value(
                'queries'), result['queries'])
            self.assertEquals(example.expected_value(
                'answers'), result['answers'])
            self.assertItemsEqual(example.expected_value(
                'AloneAnswers'), result['AloneAnswers'])
            self.assertItemsEqual(example.expected_value(
                'AloneQueries'), result['AloneQueries'])

            self.__p1.reset()

    def test_data_without_queries(self):
        self.reinit()

        example = self.data_without_queries()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(example.expected_value('queries'), result['queries'])
        self.assertEquals(example.expected_value('answers'), result['answers'])
        self.assertItemsEqual(example.expected_value(
            'AloneAnswers'), result['AloneAnswers'])
        self.assertItemsEqual(example.expected_value(
            'AloneQueries'), result['AloneQueries'])

    def test_data_without_answers(self):
        self.reinit()

        example = self.data_without_answers()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(example.expected_value('queries'), result['queries'])
        self.assertEquals(example.expected_value('answers'), result['answers'])
        self.assertItemsEqual(example.expected_value(
            'AloneAnswers'), result['AloneAnswers'])
        self.assertItemsEqual(example.expected_value(
            'AloneQueries'), result['AloneQueries'])

    def test_data_without_alone_packets(self):
        self.reinit()

        example = self.data_without_alonePackets()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(example.expected_value('queries'), result['queries'])
        self.assertEquals(example.expected_value('answers'), result['answers'])
        self.assertItemsEqual(example.expected_value(
            'AloneAnswers'), result['AloneAnswers'])
        self.assertItemsEqual(example.expected_value(
            'AloneQueries'), result['AloneQueries'])

    def test_file(self):
        self.reinit()

        self.assertEquals(self.__stringbuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
