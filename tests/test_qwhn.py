__author__ = 'sking32'

import unittest
import StringIO

from packetsexample import PacketsExample
from prers.qwhn import QueriesWithUnderscoredName
from core.packet import Packet

class TestQueriesWithUnderscoredName(unittest.TestCase):

    def reInit(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = QueriesWithUnderscoredName(self.__stringBuffer1)
        self.__p2 = QueriesWithUnderscoredName(self.__stringBuffer2)

    def dataExample(self):

        data = PacketsExample()

        data.putInformation('problematicQNames', {'www.ni_c.cl', 'www.nic_labs.cl', 'www._jerry_.cl', 'www._pinky.cl'})

        #Problems with qnames
        data.addPacket({'dest' : 'encrypted(dnsip1)', 'source' : 'encrypted(ip1)','flags': '0', 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}]})
        data.setExpected('www.ni_c.cl', [{'server' : 'encrypted(dnsip1)', 'sender' : 'encrypted(ip1)','query': {'qname' : 'www.ni_c.cl', 'qtype' : '1'}}])

        data.addPacket({'dest' : 'encrypted(dnsip2)', 'source' : 'encrypted(ip2)','flags': '0', 'queries' : [{'qname' : 'www.nic_labs.cl', 'qtype' : '2'}]})
        data.setExpected('www.nic_labs.cl', [{'server' : 'encrypted(dnsip2)', 'sender' : 'encrypted(ip2)','query': {'qname' : 'www.nic_labs.cl', 'qtype' : '2'}}])

        data.addPacket({'dest' : 'encrypted(dnsip3)', 'source' : 'encrypted(ip3)','flags': '0', 'queries' : [{'qname' : 'www._jerry_.cl', 'qtype' : '6'}]})
        data.setExpected('www._jerry_.cl', [{'server' : 'encrypted(dnsip3)', 'sender' : 'encrypted(ip3)','query': {'qname' : 'www._jerry_.cl', 'qtype' : '6'}}])

        data.addPacket({'dest' : 'encrypted(dnsip4)', 'source' : 'encrypted(ip4)','flags': '0', 'queries' : [{'qname' : 'www._pinky.cl', 'qtype' : 'f'}]})
        data.setExpected('www._pinky.cl', [{'server' : 'encrypted(dnsip4)', 'sender' : 'encrypted(ip4)','query': {'qname' : 'www._pinky.cl', 'qtype' : 'f'}}])

        #Normal data, critical qtypes
        data.addPacket({'dest' : 'encrypted(dnsip1)', 'source' : 'encrypted(ip1)','flags': '0', 'queries' : [{'qname' : 'www.nic.cl', 'qtype' : '1'}]})
        data.addPacket({'dest' : 'encrypted(dnsip2)', 'source' : 'encrypted(ip2)','flags': '0', 'queries' : [{'qname' : 'www.niclabs.cl', 'qtype' : '2'}]})
        data.addPacket({'dest' : 'encrypted(dnsip3)', 'source' : 'encrypted(ip3)','flags': '0', 'queries' : [{'qname' : 'www.jerry.cl', 'qtype' : '6'}]})
        data.addPacket({'dest' : 'encrypted(dnsip4)', 'source' : 'encrypted(ip4)','flags': '0', 'queries' : [{'qname' : 'www.pinky.cl', 'qtype' : 'f'}]})

        #Normal data
        data.addPacket({'dest' : 'encrypted(dnsip1)', 'source' : 'encrypted(ip1)','flags': '0', 'queries' : [{'qname' : 'www.nic.cl', 'qtype' : '3'}]})
        data.addPacket({'dest' : 'encrypted(dnsip2)', 'source' : 'encrypted(ip2)','flags': '8000', 'queries' : [{'qname' : 'www.niclabs.cl', 'qtype' : '4'}]})
        data.addPacket({'dest' : 'encrypted(dnsip3)', 'source' : 'encrypted(ip3)','flags': '0', 'queries' : [{'qname' : 'www.jerry.cl', 'qtype' : '5'}]})
        data.addPacket({'dest' : 'encrypted(dnsip4)', 'source' : 'encrypted(ip4)','flags': '8000', 'queries' : [{'qname' : 'www.pinky.cl', 'qtype' : '7'}]})

        #Underscore data, noncritical qtypes
        data.addPacket({'dest' : 'encrypted(dnsip1)', 'source' : 'encrypted(ip1)','flags': '0', 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '3'}]})
        data.addPacket({'dest' : 'encrypted(dnsip2)', 'source' : 'encrypted(ip2)','flags': '0', 'queries' : [{'qname' : 'www.nic_labs.cl', 'qtype' : '4'}]})
        data.addPacket({'dest' : 'encrypted(dnsip3)', 'source' : 'encrypted(ip3)','flags': '0', 'queries' : [{'qname' : 'www._jerry_.cl', 'qtype' : '5'}]})
        data.addPacket({'dest' : 'encrypted(dnsip4)', 'source' : 'encrypted(ip4)','flags': '0', 'queries' : [{'qname' : 'www._pinky.cl', 'qtype' : '7'}]})

        #Answers
        data.addPacket({'dest' : 'encrypted(ip1)', 'source' : 'encrypted(dnsip1)','flags': '8000', 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}]})
        data.addPacket({'dest' : 'encrypted(ip2)', 'source' : 'encrypted(dnsip2)','flags': '8000', 'queries' : [{'qname' : 'www.niclabs.cl', 'qtype' : '2'}]})
        data.addPacket({'dest' : 'encrypted(ip3)', 'source' : 'encrypted(dnsip3)','flags': '8000', 'queries' : [{'qname' : 'www.jerry.cl', 'qtype' : '5'}]})
        data.addPacket({'dest' : 'encrypted(ip4)', 'source' : 'encrypted(dnsip4)','flags': '8000', 'queries' : [{'qname' : 'www._pinky.cl', 'qtype' : '7'}]})


        return data


    def dataDifferenCase(self):
        data = PacketsExample()
        data.putInformation('problematicQName','www.ni_c.cl')

        expectedList = []

        data.addPacket({'dest' : 'encrypted(dnsip1)', 'source' : 'encrypted(ip1)','flags': '0', 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}]})
        expectedList.append({'server' : 'encrypted(dnsip1)', 'sender' : 'encrypted(ip1)','query': {'qname' : 'www.ni_c.cl', 'qtype' : '1'}})

        data.addPacket({'dest' : 'encrypted(dnsip1)', 'source' : 'encrypted(ip1)','flags': '0', 'queries' : [{'qname' : 'WWW.NI_C.CL', 'qtype' : '1'}]})
        expectedList.append({'server' : 'encrypted(dnsip1)', 'sender' : 'encrypted(ip1)','query': {'qname' : 'WWW.NI_C.CL', 'qtype' : '1'}})

        data.setExpected('www.ni_c.cl', expectedList)


        data.addPacket({'dest' : 'encrypted(dnsip1)', 'source' : 'encrypted(ip1)','flags': '0', 'queries' : [{'qname' : 'wwww.ni_c.cl', 'qtype' : '1'}]})
        data.addPacket({'dest' : 'encrypted(dnsip1)', 'source' : 'encrypted(ip1)','flags': '0', 'queries' : [{'qname' : 'WWW:NI_C.CL', 'qtype' : '1'}]})

        return data

    def dataRepeatError(self):
        data = PacketsExample()
        data.putInformation('problematicQNames', {'www.ni_c.cl', 'www.nic_labs.cl'})

        expectedList = []
        for i in range (3) :
            data.addPacket({'dest' : 'encrypted(dnsip1)', 'source' : 'encrypted(ip1)','flags': '0', 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}]})
            expectedList.append({'server' : 'encrypted(dnsip1)', 'sender' : 'encrypted(ip1)','query': {'qname' : 'www.ni_c.cl', 'qtype' : '1'}})
        data.setExpected('www.ni_c.cl', expectedList)

        expectedList = []
        for i in range(2) :
            data.addPacket({'dest' : 'encrypted(dnsip2)', 'source' : 'encrypted(ip2)','flags': '0', 'queries' : [{'qname' : 'www.nic_labs.cl', 'qtype' : '2'}]})
            expectedList.append({'server' : 'encrypted(dnsip2)', 'sender' : 'encrypted(ip2)','query': {'qname' : 'www.nic_labs.cl', 'qtype' : '2'}})
        data.setExpected('www.nic_labs.cl', expectedList)

        return  data

    def setUp(self):
        self.reInit()


    def test_rightFormat(self):
        self.reInit()

        self.__p1(Packet({'dest' : 'encrypted(dnsip1)', 'source' : 'encrypted(ip1)','flags': '0', 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}]}))
        result = self.__p1.get_data()

        self.assertEquals(type(result), dict)

        resultForQName = result['www.ni_c.cl']
        self.assertEquals(type(resultForQName), list)

        someQuery = resultForQName[0]
        self.assertEquals(type(someQuery), dict)

        self.assertTrue(someQuery.has_key('query'))
        self.assertTrue(someQuery.has_key('sender'))
        self.assertTrue(someQuery.has_key('server'))

        queryItself = someQuery['query']

        self.assertTrue(queryItself.has_key('qtype'))
        self.assertTrue(queryItself.has_key('qname'))



    def test_noData(self):
        self.reInit()

        result = self.__p1.get_data()

        self.assertEquals({}, result)

    def test_sameBehavior(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)
            self.__p2(packet)

        result1 = self.__p1.get_data()
        result2 = self.__p2.get_data()

        self.assertTrue(result1, result2)

    def test_dataExample(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        expectedProblematic = example.getInformation('problematicQNames')

        for source in result.keys():
            self.assertTrue(source in expectedProblematic)

        for source in  expectedProblematic:
            self.assertTrue(result.has_key(source))
            self.assertEquals(example.expectedValue(source), result[source])

    def test_dataDifferenCase(self):
        self.reInit()

        example = self.dataDifferenCase()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        expectedProblematic = example.getInformation('problematicQName')


        self.assertTrue(result.has_key(expectedProblematic))
        self.assertItemsEqual(example.expectedValue(expectedProblematic), result[expectedProblematic])

    def test_dataRepeatError(self):
        self.reInit()

        example = self.dataRepeatError()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        expectedProblematic = example.getInformation('problematicQNames')

        for source in  expectedProblematic:
            self.assertTrue(result.has_key(source))
            self.assertEquals(example.expectedValue(source), result[source])


    def test_reset(self):
        self.reInit()

        example = self.dataExample()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()
            expectedProblematic = example.getInformation('problematicQNames')

            for source in result.keys():
                self.assertTrue(source in expectedProblematic)

            for source in  expectedProblematic:
                self.assertTrue(result.has_key(source))
                self.assertEquals(example.expectedValue(source), result[source])

            self.__p1.reset()

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
