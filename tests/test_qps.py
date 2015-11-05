import unittest
import StringIO
from time import time

from packetsexample import PacketsExample
from prers import QueriesPerSecond


class TestQueriesPerSecond(unittest.TestCase):

    def reinit(self):
        self.__stringbuffer1 = StringIO.StringIO()
        self.__stringbuffer2 = StringIO.StringIO()
        self.__p1 = QueriesPerSecond(self.__stringbuffer1)
        self.__p2 = QueriesPerSecond(self.__stringbuffer2)

    def data_example(self):
        na = 2
        nq = 2
        data = PacketsExample({'na': na, 'nq': nq})

        for i in range(na):
            data.add_packet({'flags': '8000'})
        for i in range(nq):
            data.add_packet({'flags': '0'})

        return data

    def data_only_queries(self):
        na = 0
        nq = 2
        data = PacketsExample({'na': na, 'nq': nq})

        data = PacketsExample()
        for i in range(nq):
            data.add_packet({'flags': '0'})

        return data

    def data_only_answers(self):
        na = 2
        nq = 0
        data = PacketsExample({'na': na, 'nq': nq})

        for i in range(na):
            data.add_packet({'flags': '8000'})

        return data

    def setUp(self):
        self.reinit()

    def test_right_format(self):
        self.reinit()

        result = self.__p1.get_data()

        self.assertEquals(type(result), dict)
        self.assertTrue('qps' in result)
        self.assertEqual(type(result['qps']), float)
        self.assertGreaterEqual(result['qps'], 0)

    def test_no_data(self):
        self.reinit()

        result = self.__p1.get_data()

        self.assertEqual(result['qps'], 0)

    def test_data_example(self):

        before_init_time = time()
        self.reinit()
        after_init_time = time()

        example = self.data_example()

        for packet in example:
            self.__p1(packet)

        before_end_time = time()
        result = self.__p1.get_data()
        after_end_time = time()

        self.assertLessEqual(example.expected_value(
            'nq') / (after_end_time - before_init_time), result['qps'])
        self.assertGreaterEqual(example.expected_value(
            'nq') / (before_end_time - after_init_time), result['qps'])

    def test_data_only_answers(self):

        self.reinit()

        example = self.data_only_answers()

        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()

        self.assertLessEqual(result['qps'], 0)

    def test_data_only_queries(self):

        before_init_time = time()
        self.reinit()
        after_init_time = time()

        example = self.data_only_answers()

        for packet in example:
            self.__p1(packet)

        before_end_time = time()
        result = self.__p1.get_data()
        after_end_time = time()

        self.assertLessEqual(example.expected_value(
            'nq') / (after_end_time - before_init_time), result['qps'])
        self.assertGreaterEqual(example.expected_value(
            'nq') / (before_end_time - after_init_time), result['qps'])

    def test_reset(self):
        before_init_time = time()
        self.reinit()
        after_init_time = time()

        example = self.data_example()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            before_end_time = time()
            result = self.__p1.get_data()
            after_end_time = time()

            self.assertLessEqual(example.expected_value(
                'nq') / (after_end_time - before_init_time), result['qps'])
            self.assertGreaterEqual(example.expected_value(
                'nq') / (before_end_time - after_init_time), result['qps'])

            before_init_time = time()
            self.__p1.reset()
            after_init_time = time()

    def test_file(self):
        self.reinit()

        self.assertEquals(self.__stringbuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
