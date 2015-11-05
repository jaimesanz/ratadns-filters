from random import shuffle
from core import Packet


class PacketsExample:
    """Help on testing.

    Encapsulates packets given to PreRs
    with their expected results
    """

    def __init__(self, expected={}, information={}):
        self.__data = []
        self.__expected = expected
        self.__information = information
        self.__same_order = False

    def __iter__(self):
        if not(self.__same_order):
            shuffle(self.__data)
        return self.__data.__iter__()

    def do_not_change_order(self):
        self.__same_order = True

    def add_packet(self, d):
        self.__data.append(Packet(d))

    def set_expected(self, key, value):
        self.__expected[key] = value

    def put_information(self, key, value):
        self.__information[key] = value

    def get_information(self, key):
        return self.__information[key]

    def expected_value(self, key):
        if key not in self.__expected:
            raise ExpectedValueNotSetError(
                'Value ' + key + ' was not set previusly')
        return self.__expected[key]


class ExpectedValueNotSetError(Exception):
    pass
