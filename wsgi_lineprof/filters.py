from abc import ABCMeta, abstractproperty

import six


@six.add_metaclass(ABCMeta)
class BaseFilter(object):
    @abstractproperty
    def filter_function(self):
        return


class FilenameFilter(BaseFilter):
    """Filter which matches with filename"""
    def __init__(self, filename):
        self.filename = filename

    def filter_function(self):
        return lambda stat: self.filename in stat.filename


class NameFilter(BaseFilter):
    """Filter which matches with name"""
    def __init__(self, name):
        self.name = name

    def filter_function(self):
        return lambda stat: self.name in stat.name
