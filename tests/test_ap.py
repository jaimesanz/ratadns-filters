__author__ = 'sking32'

import unittest

class TestAlonePackets(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_example(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
