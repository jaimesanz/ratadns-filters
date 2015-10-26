import unittest

from packetsexample import PacketsExample
from core import Packet
from core import PacketWithoutInfoError


class TestQueriesNameCounter(unittest.TestCase):

    def setUp(self):
        pass

    def test_has_info(self):
        info = {}
        info['id'] = 'id'
        info['queries'] = [{'qname': 'qname'}]
        info['source'] = 'source'
        info['dest'] = 'dest'

        a = Packet(info, 1000)
        self.assertEqual(a.input, info)
        self.assertEqual(a.id, info['id'])
        self.assertEqual(a.qname, info['queries'][0]['qname'])
        self.assertEqual(a.query, info['queries'][0])
        self.assertEqual(a.source, info['source'])
        self.assertEqual(a.dest, info['dest'])
        self.assertEqual(a.window_size, 1000)

    def test_does_not_have_info(self):
        info = {}

        a = Packet(info, 1000)

        with self.assertRaises(PacketWithoutInfoError):
            a.id

        with self.assertRaises(PacketWithoutInfoError):
            a.qname

        with self.assertRaises(PacketWithoutInfoError):
            a.query

        with self.assertRaises(PacketWithoutInfoError):
            a.source

        with self.assertRaises(PacketWithoutInfoError):
            a.dest

        with self.assertRaises(PacketWithoutInfoError):
            a.dest

        with self.assertRaises(PacketWithoutInfoError):
            a.is_answer()

        with self.assertRaises(PacketWithoutInfoError):
            a.is_critical_type()

    def test_methods(self):
        queryProblematic = {'dest': 'encrypted(dnsip1)',
                            'source': 'encrypted(ip1)',
                            'flags': '0',
                            'queries': [
                                {'qname': 'www.ni_c.cl', 'qtype': '1'}]}
        answer = {'dest': 'encrypted(ip3)',
                  'source': 'encrypted(dnsip3)',
                  'flags': '8000',
                  'queries': [
                      {'qname': 'www.jerry.cl', 'qtype': '5'}]}

        q = Packet(queryProblematic)
        a = Packet(answer)

        self.assertTrue(q.is_critical_type())
        self.assertTrue(a.is_answer())

        self.assertFalse(a.is_critical_type())
        self.assertFalse(q.is_answer())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
