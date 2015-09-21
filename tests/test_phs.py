__author__ = 'sking32'

import unittest
import StringIO

from packetsexample import PacketsExample
from prers.phs import PacketHasUnderscore


class TestPacketHasUnderscore(unittest.TestCase):

    def reInit(self):
        self.__stringBuffer1 = StringIO.StringIO()
        self.__stringBuffer2 = StringIO.StringIO()
        self.__p1 = PacketHasUnderscore(self.__stringBuffer1)
        self.__p2 = PacketHasUnderscore(self.__stringBuffer2)

    def dataExample(self):

        data = PacketsExample()
        data.putInformation('problematicSources', {'encrypted(www.ni_c.cl)' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}],
                                                'encrypted(www.nic_labs.cl)' : [{'qname' : 'www.nic_labs.cl', 'qtype' : '2'}],
                                                'encrypted(www._jerry_.cl)' : [{'qname' : 'www._jerry_.cl', 'qtype' : '6'}],
                                                'encrypted(www._pinky.cl)' : [{'qname' : 'www._pinky.cl', 'qtype' : 'f'}]})

        #Problems with qnames
        data.addPacket({'source' : 'encrypted(www.ni_c.cl)','flags': '0', 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}]})
        data.setExpected('encrypted(www.ni_c.cl)',  {"cnt": 1, 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}]})

        data.addPacket({'source' : 'encrypted(www.nic_labs.cl)','flags': '0', 'queries' : [{'qname' : 'www.nic_labs.cl', 'qtype' : '2'}]})
        data.setExpected('encrypted(www.nic_labs.cl)',  {"cnt": 1, 'queries' : [{'qname' : 'www.nic_labs.cl', 'qtype' : '1'}]})

        data.addPacket({'source' : 'encrypted(www._jerry_.cl)','flags': '0', 'queries' : [{'qname' : 'www._jerry_.cl', 'qtype' : '6'}]})
        data.setExpected('encrypted(www._jerry_.cl)',  {"cnt": 1, 'queries' : [{'qname' : 'www._jerry_.cl', 'qtype' : '1'}]})

        data.addPacket({'source' : 'encrypted(www._pinky.cl)','flags': '0', 'queries' : [{'qname' : 'www._pinky.cl', 'qtype' : 'f'}]})
        data.setExpected('encrypted(www._pinky.cl)',  {"cnt": 1, 'queries' : [{'qname' : 'www._pinky.cl', 'qtype' : '1'}]})

        #Normal data, critical qtypes
        data.addPacket({'source' : 'encrypted(www.nic.cl)','flags': '0', 'queries' : [{'qname' : 'www.nic.cl', 'qtype' : '1'}]})
        data.addPacket({'source' : 'encrypted(www.niclabs.cl)','flags': '0', 'queries' : [{'qname' : 'www.niclabs.cl', 'qtype' : '2'}]})
        data.addPacket({'source' : 'encrypted(www.jerry.cl)','flags': '0', 'queries' : [{'qname' : 'www.jerry.cl', 'qtype' : '6'}]})
        data.addPacket({'source' : 'encrypted(www.pinky.cl)','flags': '0', 'queries' : [{'qname' : 'www.pinky.cl', 'qtype' : 'f'}]})

        #Normal data
        data.addPacket({'source' : 'encrypted(www.nic.cl)','flags': '0', 'queries' : [{'qname' : 'www.nic.cl', 'qtype' : '3'}]})
        data.addPacket({'source' : 'encrypted(www.niclabs.cl)','flags': '8000', 'queries' : [{'qname' : 'www.niclabs.cl', 'qtype' : '4'}]})
        data.addPacket({'source' : 'encrypted(www.jerry.cl)','flags': '0', 'queries' : [{'qname' : 'www.jerry.cl', 'qtype' : '5'}]})
        data.addPacket({'source' : 'encrypted(www.pinky.cl)','flags': '8000', 'queries' : [{'qname' : 'www.pinky.cl', 'qtype' : '7'}]})

        #Underscore data, noncritical qtypes
        data.addPacket({'source' : 'encrypted(www.ni_c.cl)','flags': '0', 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '3'}]})
        data.addPacket({'source' : 'encrypted(www.nic_labs.cl)','flags': '0', 'queries' : [{'qname' : 'www.nic_labs.cl', 'qtype' : '4'}]})
        data.addPacket({'source' : 'encrypted(www._jerry_.cl)','flags': '0', 'queries' : [{'qname' : 'www._jerry_.cl', 'qtype' : '5'}]})
        data.addPacket({'source' : 'encrypted(_www.pinky.cl)','flags': '0', 'queries' : [{'qname' : 'www._pinky.cl', 'qtype' : '7'}]})

        #Answers
        data.addPacket({'source' : 'encrypted(www.ni_c.cl)','flags': '8000', 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}]})
        data.addPacket({'source' : 'encrypted(www.niclabs.cl)','flags': '8000', 'queries' : [{'qname' : 'www.niclabs.cl', 'qtype' : '2'}]})
        data.addPacket({'source' : 'encrypted(www.jerry.cl)','flags': '8000', 'queries' : [{'qname' : 'www.jerry.cl', 'qtype' : '5'}]})
        data.addPacket({'source' : 'encrypted(_www.pinky.cl)','flags': '8000', 'queries' : [{'qname' : 'www._pinky.cl', 'qtype' : '7'}]})


        return data


    def dataRepeatError(self):
        data = PacketsExample()

        data.putInformation('problematicSources', {'encrypted(www.ni_c.cl)' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}],
                                                'encrypted(www.nic_labs.cl)' : [{'qname' : 'www.nic_labs.cl', 'qtype' : '2'}]})

        countOfErrors = {}

        for i in range (3) :
            data.addPacket({'source' : 'encrypted(www.ni_c.cl)','flags': '0', 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}]})
        countOfErrors['encrypted(www.ni_c.cl)'] = 3

        for i in range(2) :
            data.addPacket({'source' : 'encrypted(www.nic_labs.cl)','flags': '0', 'queries' : [{'qname' : 'www.nic_labs.cl', 'qtype' : '2'}]})
        countOfErrors['encrypted(www.nic_labs.cl)'] = 2

        data.putInformation('countOfErrors', countOfErrors)
        return  data

    def setUp(self):
        self.reInit()


    def test_rightFormat(self):
        self.reInit()

        self.__p1({'source' : 'encrypted(www.ni_c.cl)','flags': '0', 'queries' : [{'qname' : 'www.ni_c.cl', 'qtype' : '1'}]})
        result = self.__p1.get_data()

        self.assertEquals(type(result), dict)

        resultForSource = result['encrypted(www.ni_c.cl)']
        self.assertEquals(type(resultForSource), dict)
        self.assertTrue(resultForSource.has_key('cnt'))
        self.assertTrue(resultForSource.has_key('queries'))

        self.assertGreater(resultForSource['cnt'], 0)

        queries = resultForSource['queries']
        self.assertEquals(type(queries), list)
        self.assertGreater(len(queries), 0)

        queryExample = queries[0]
        self.assertTrue(queryExample.has_key('qtype'))
        self.assertTrue(queryExample.has_key('qname'))




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

        self.assertTrue(result1, result2) #DOES IT WORK? #DOES THE 'FOR' WORK TO TEST SAME BEHAVIOR?

    def test_dataExample(self):
        self.reInit()

        example = self.dataExample()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        expectedProblematic = example.getInformation('problematicSources')

        for source in result.keys():
            self.assertTrue(expectedProblematic.has_key(source))

        for source in  expectedProblematic.keys():
            self.assertTrue(result.has_key(source))
            expectedQueries = expectedProblematic[source]
            self.assertEquals(len(expectedQueries), result[source]['cnt'])
            self.assertEquals(len(expectedQueries), len(result[source]['queries']))
            self.assertListEqual(expectedQueries, result[source]['queries'])


    def test_dataRepeatError(self):
        self.reInit()

        example = self.dataRepeatError()
        for packet in example:
            self.__p1(packet)

        result = self.__p1.get_data()
        expectedProblematic = example.getInformation('problematicSources')
        expectedCnt = example.getInformation('countOfErrors')

        for source in  expectedProblematic.keys():
            self.assertTrue(result.has_key(source))
            expectedQueries = expectedProblematic[source]
            self.assertEquals(expectedCnt[source], result[source]['cnt'])
            self.assertEquals(result[source]['cnt'], len(result[source]['queries']))
            for query in result[source]['queries'] :
                self.assertEqual(expectedQueries[0], query)


    def test_reset(self):
        self.reInit()

        example = self.dataExample()

        for i in range(2):
            for packet in example:
                self.__p1(packet)

            result = self.__p1.get_data()
            expectedProblematic = example.getInformation('problematicSources')

            for source in result.keys():
                self.assertTrue(expectedProblematic.has_key(source))

            for source in  expectedProblematic.keys():
                self.assertTrue(result.has_key(source))
                expectedQueries = expectedProblematic[source]
                self.assertEquals(len(expectedQueries), result[source]['cnt'])
                self.assertListEqual(expectedQueries, result[source]['queries'])

            self.__p1.reset()

    def test_file(self):
        self.reInit()

        self.assertEquals(self.__stringBuffer1, self.__p1.get_file())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
