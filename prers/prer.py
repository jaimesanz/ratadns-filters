__author__ = 'sking32'


class PreR(object):
    """Implement transformation of the packet-analyzer output.

    The PreR object knows how to
    process one packet at a time,
    give the current result and
    reset its own state.
    """

    def __init__(self, f):
        self.__f = f

    def __call__(self, p):
        raise NotImplementedError('Method __call__ not implemented')

    def get_data(self):
        raise NotImplementedError('Method get_data not implemented')

    def get_file(self):
        return self.__f

    def reset(self):
        raise NotImplementedError('Method reset not implemented')
