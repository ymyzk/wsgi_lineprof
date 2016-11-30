from io import TextIOWrapper  # noqa: F401
import sys
from typing import Callable, Iterable, TextIO, Union  # noqa: F401

from wsgi_lineprof.profiler import LineProfiler
from wsgi_lineprof.stats import FilterType  # noqa: F401


class LineProfilerMiddleware(object):
    def __init__(self,
                 app,  # type: Callable
                 stream=None,  # type: Union[TextIO, TextIOWrapper]
                 filters=tuple()  # type: Iterable[FilterType]
                 ):
        self.app = app
        self.stream = sys.stdout if stream is None else stream
        self.filters = filters

    def __call__(self, env, start_response):
        profiler = LineProfiler()

        profiler.enable()
        result = self.app(env, start_response)
        profiler.disable()

        stats = profiler.get_stats()

        for f in self.filters:
            stats = stats.filter(f)

        stats.write_text(self.stream)

        return result
