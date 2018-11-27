from abc import ABCMeta, abstractmethod
from itertools import islice
from operator import attrgetter
import re
from typing import Iterable, TYPE_CHECKING  # noqa: F401

from six import add_metaclass
from six.moves import filter


if TYPE_CHECKING:
    from wsgi_lineprof.stats import LineProfilerStat  # noqa: F401


@add_metaclass(ABCMeta)
class BaseFilter(object):
    @abstractmethod
    def filter(self, stats):
        # type: (Iterable[LineProfilerStat]) -> Iterable[LineProfilerStat]
        pass


class FilenameFilter(BaseFilter):
    """Filter which matches with filename"""
    def __init__(self, filename, regex=False):
        # type: (str, bool) -> None
        self.filename = filename
        self.regex = regex
        self.compiled_regex = re.compile(filename)

    def filter(self, stats):
        # type: (Iterable[LineProfilerStat]) -> Iterable[LineProfilerStat]
        if self.regex:
            compiled_regex = self.compiled_regex
            return filter(lambda s: compiled_regex.search(s.filename), stats)
        else:
            return filter(lambda s: self.filename in s.filename, stats)


class NameFilter(BaseFilter):
    """Filter which matches with name"""
    def __init__(self, name, regex=True):
        # type: (str, bool) -> None
        self.name = name
        self.regex = regex
        self.compiled_regex = re.compile(name)

    def filter(self, stats):
        # type: (Iterable[LineProfilerStat]) -> Iterable[LineProfilerStat]
        if self.regex:
            compiled_regex = self.compiled_regex
            return filter(lambda s: compiled_regex.search(s.name), stats)
        else:
            return filter(lambda s: self.name in s.name, stats)


class TotalTimeSorter(BaseFilter):
    """Sort stats by total time"""
    def __init__(self, reverse=True):
        # type: (bool) -> None
        self.reverse = reverse

    def filter(self, stats):
        # type: (Iterable[LineProfilerStat]) -> Iterable[LineProfilerStat]
        return sorted(stats,
                      key=attrgetter("total_time"), reverse=self.reverse)


class TopItemsFilter(BaseFilter):
    """Get first n stats"""
    def __init__(self, n=10):
        # type: (int) -> None
        self.n = n

    def filter(self, stats):
        # type: (Iterable[LineProfilerStat]) -> Iterable[LineProfilerStat]
        return islice(stats, self.n)
