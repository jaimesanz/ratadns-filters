import unittest
from packetsexample import PacketsExample
import StringIO
from prers.packetsummary import PacketSummary

__author__ = 'franchoco'

class TestPacketSummary(unittest.TestCase):
    def setUp(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__p1 = PacketSummary(self.__stringBuffer1)

    def test_example(self):
        expected_output = {
            "1": {
                "bec47b2d": ["www.nic.cl.", "uchile.cl.", "tests.cl."],
                "c800aec8": ["ns.ns.cl.", "ns.ns.cl."]
            },
            "10": {
                "bec47b2d": ["www.www.cl."],
                "c81b0202": ["qwerty.cl.", "azerty.cl."],
                "ba43f806": ["google.cl."]
            }
        }

        data = PacketsExample(expected_output)

        data.do_not_change_order()

        data.add_packet({"source": "bec47b2d",
                         "flags": "0",
                         "queries": [
                             {"qname": "www.nic.cl.", "qtype": "1"}
                         ]})
        data.add_packet({"source": "bec47b2d",
                         "flags": "8000",
                         "queries": [
                             {"qname": "www.nic.cl.", "qtype": "1"}
                         ]})
        data.add_packet({"source": "bec47b2d",
                         "flags": "0",
                         "queries": [
                             {"qname": "uchile.cl.", "qtype": "1"}
                         ]})
        data.add_packet({"source": "bec47b2d",
                         "flags": "0",
                         "queries": [
                             {"qname": "tests.cl.", "qtype": "1"}
                         ]})
        data.add_packet({"source": "c800aec8",
                         "flags": "0",
                         "queries": [
                             {"qname": "ns.ns.cl.", "qtype": "1"}
                         ]})
        data.add_packet({"source": "c800aec8",
                         "flags": "0",
                         "queries": [
                             {"qname": "ns.ns.cl.", "qtype": "1"}
                         ]})
        data.add_packet({"source": "bec47b2d",
                         "flags": "0",
                         "queries": [
                             {"qname": "www.www.cl.", "qtype": "10"}
                         ]})
        data.add_packet({"source": "c81b0202",
                         "flags": "0",
                         "queries": [
                             {"qname": "qwerty.cl.", "qtype": "10"}
                         ]})
        data.add_packet({"source": "c81b0202",
                         "flags": "0",
                         "queries": [
                             {"qname": "azerty.cl.", "qtype": "10"}
                         ]})
        data.add_packet({"source": "c81b0202",
                         "flags": "8000",
                         "queries": [
                             {"qname": "awerty.cl.", "qtype": "10"}
                         ]})
        data.add_packet({"source": "c81ba202",
                         "flags": "8000",
                         "queries": [
                             {"qname": "awerdasdasty.cl.", "qtype": "10"}
                         ]})
        data.add_packet({"source": "c81bb202",
                         "flags": "8000",
                         "queries": [
                             {"qname": "awrqwereqwrerty.cl.", "qtype": "10"}
                         ]})
        data.add_packet({"source": "ba43f806",
                         "flags": "0",
                         "queries": [
                             {"qname": "google.cl.", "qtype": "10"}
                         ]})

        for packet in data:
            self.__p1(packet)

        result = self.__p1.get_data()
        self.assertDictEqual(expected_output, result)


if __name__ == '__main__':
    unittest.main()
