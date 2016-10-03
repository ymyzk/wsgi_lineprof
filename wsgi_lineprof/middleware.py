import sys
from wsgi_lineprof.profiler import LineProfiler


class LineProfilerMiddleware(object):
    def __init__(self, app, stream=None):
        self.app = app
        self.stream = sys.stdout if stream is None else stream

    def __call__(self, env, start_response):
        profiler = LineProfiler()

        profiler.enable()
        result = self.app(env, start_response)
        profiler.disable()

        profiler.get_stats().write_text(self.stream)

        return result
