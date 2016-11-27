from abc import ABCMeta, abstractmethod
from itertools import islice
from operator import attrgetter

from six import add_metaclass
from six.moves import filter


@add_metaclass(ABCMeta)
class BaseFilter(object):
    @abstractmethod
    def filter(self, stats):
        return


class FilenameFilter(BaseFilter):
    """Filter which matches with filename"""
    def __init__(self, filename):
        self.filename = filename

    def filter(self, stats):
        return filter(lambda s: self.filename in s.filename, stats)


class NameFilter(BaseFilter):
    """Filter which matches with name"""
    def __init__(self, name):
        self.name = name

    def filter(self, stats):
        return filter(lambda s: self.name in s.name, stats)


class TotalTimeSorter(BaseFilter):
    """Sort stats by total time"""
    def __init__(self, reverse=True):
        self.reverse = reverse

    def filter(self, stats):
        return sorted(stats,
                      key=attrgetter("total_time"), reverse=self.reverse)


class TopItemsFilter(BaseFilter):
    """Get first n stats"""
    def __init__(self, n=10):
        self.n = n

    def filter(self, stats):
        return islice(stats, self.n)
