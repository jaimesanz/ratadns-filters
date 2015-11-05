import unittest
import StringIO
import operator

from packetsexample import PacketsExample
from prers import TopNQ


class TestTopNQ(unittest.TestCase):

    def reinit(self, n1=3, n2=3):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__stringbuffer2 = StringIO.StringIO()
        self.__p1 = TopNQ(self.__stringbuffer1, n=n1)
        self.__p2 = TopNQ(self.__stringbuffer2, n=n2)

    def data_example(self):

        queries = {'www.nic.cl': 5, 'www.niclabs.cl': 4,
                   'www.uchile.cl': 3, 'www.jerry.cl': 3, 'www.pinky.cl': 2}
        data = PacketsExample(queries)

        # Returns a list with the elements of
        # the dict in descending order of its keys
        data.put_information('sortedQnames',
                             map(list, sorted(queries.items(),
                                              key=operator.itemgetter(
                                 1), reverse=True)))

        for i in range(5):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.nic.cl'}]})

        for i in range(4):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.niclabs.cl'}]})

        for i in range(3):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.uchile.cl'}]})

        for i in range(3):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.jerry.cl'}]})

        for i in range(2):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.pinky.cl'}]})

        data.add_packet({'flags': '8000', 'queries': [
            {'qname': 'www.nic.cl'}]})  # Answers
        data.add_packet({'flags': '8000', 'queries': [
            {'qname': 'www.brain.cl'}]})
        data.add_packet({'flags': '8000', 'queries': [
            {'qname': 'www.pinky.cl'}]})

        return data

    def data_different_case(self):
        queries = {'www.nic.cl': 10, 'www.niclabs.cl': 5, 'wwww.niclabs.cl': 6}
        data = PacketsExample(queries)
        # Returns a list with the elements of
        # the dict in descending order of its keys
        data.put_information('sortedQnames',
                             map(list, sorted(queries.items(),
                                              key=operator.itemgetter(
                                 1), reverse=True)))

        for i in range(5):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.nic.cl'}]})
        for i in range(5):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'WWW.NIC.CL'}]})

        for i in range(5):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.niclabs.cl'}]})
        for i in range(6):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'WwWW.NicLaBs.cl'}]})

        return data

    def data_just_answers(self):

        data = PacketsExample()
        data.add_packet({'flags': '8000', 'queries': [
            {'qname': 'www.nic.cl'}]})  # Answers
        data.add_packet({'flags': '8000', 'queries': [
            {'qname': 'www.brain.cl'}]})
        data.add_packet({'flags': '8000', 'queries': [
            {'qname': 'www.pinky.cl'}]})

        return data

    def data_equal_rating(self):
        n = 10
        queries = {'www.nic.cl': n, 'www.niclabs.cl': n,
                   'www.uchile.cl': n, 'www.jerry.cl': n, 'www.pinky.cl': n}
        data = PacketsExample(queries)
        data.put_information('equalQnames', 5)
        for i in range(n):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.nic.cl'}]})

        for i in range(n):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.niclabs.cl'}]})

        for i in range(n):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.uchile.cl'}]})

        for i in range(n):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.jerry.cl'}]})

        for i in range(n):
            data.add_packet({'flags': '0', 'queries': [
                {'qname': 'www.pinky.cl'}]})

        return data

    def setUp(self):
        self.reinit()

    def test_right_format(self):
        n = 3
        self.reinit(3)

        example = self.data_example()

        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertEquals(type(result), list)
        # Not always(when there is not enough info)
        self.assertGreaterEqual(len(result), n)

        for p in result:
            self.assertEquals(type(p), list)
            self.assertEquals(len(p), 2)
            self.assertEquals(type(p[0]), str)
            self.assertEquals(type(p[1]), int)

    def test_no_data(self):
        self.reinit()

        result = self.__p1.get_data()

        self.assertEquals([], result)

    def test_same_behavior(self):
        self.reinit()

        example = self.data_example()
        for packet in example:
            self.__p1(packet)
        for packet in example:
            self.__p2(packet)

        result1 = self.__p1.get_data()
        result2 = self.__p2.get_data()

        self.assertItemsEqual(result1, result2)

    def test_number_of_qnames(self):
        example = self.data_example()
        tops = example.get_information('sortedQnames')

        for n in range(2 * len(tops)):
            self.reinit(n)
            n = min(n, len(tops))

            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()
            self.assertGreaterEqual(len(result), n)

    def test_subset(self):
        n = 3
        self.reinit(n)

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        sub_result = self.__p1.get_data()

        self.reinit(n + 2)
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        for p in sub_result:
            self.assertTrue(p in result)

        existe_diferente = False
        for p in result:
            existe_diferente = existe_diferente or not(p in sub_result)
        self.assertTrue(existe_diferente)

    def test_equal_rating(self):
        n = 3
        self.reinit(n)

        example = self.data_equal_rating()
        for packet in example:
            self.__p1(packet)

        self.assertEquals(len(self.__p1.get_data()),
                          example.get_information('equalQnames'))

    def test_data_example(self):
        n = 4
        self.reinit(n)

        example = self.data_example()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertGreaterEqual(len(result), n)
        tops = example.get_information('sortedQnames')

        for i in range(len(result) - 1):
            self.assertGreaterEqual(result[i][1], result[i + 1][1])
        self.assertItemsEqual(tops[0:len(result)], result)

        def test_data_just_answers(self):
            self.reinit()

            example = self.data_just_answers()
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            self.assertEquals(result, [])

    def test_data_different_case(self):
        n = 3
        self.reinit(n)

        example = self.data_different_case()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        self.assertGreaterEqual(len(result), n)
        tops = example.get_information('sortedQnames')
        self.assertItemsEqual(tops[0:len(result)], result)

    def test_reset(self):
        n = 3
        self.reinit(n)

        for i in range(2):
            example = self.data_example()
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()

            self.assertGreaterEqual(len(result), n)
            tops = example.get_information('sortedQnames')
            self.assertItemsEqual(tops[0:len(result)], result)
            self.__p1.reset()

    def test_file(self):
        self.reinit()

        self.assertEquals(self.__stringbuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
