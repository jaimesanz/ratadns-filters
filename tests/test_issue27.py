
import unittest
import StringIO

from packetsexample import PacketsExample
from prers import QueriesNameCounter
from core import PacketWithoutInfoError


class TestIssue27(unittest.TestCase):

    def reInit(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = QueriesNameCounter(self.__stringBuffer1)
        self.__p2 = QueriesNameCounter(self.__stringBuffer2)

    def dataExample(self):
        data = PacketsExample()
        data.add_packet({'flags': '0', 'queries': []})

        data.set_expected('', 1)

        data.put_information('QNames', {''})
        return data

    def setUp(self):
        self.reInit()

    def test_dataExample(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            with self.assertRaises(PacketWithoutInfoError):
                self.__p1(packet)


    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
