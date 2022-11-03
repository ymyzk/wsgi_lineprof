"""Benchmarks with different filters

base: Application without LineProfilerMiddleware
no_filter: Application with LineProfilerMiddleware using no filters
filter: Application with LineProfilerMiddleware using filters
"""

from webtest import TestApp

from wsgi_lineprof.filters import FilenameFilter
from wsgi_lineprof.middleware import LineProfilerMiddleware

from .apps import fib_app, jinja_app
from .utils import StringNoopIO


class BaseTest:
    param_names = ["filters"]
    params = ["base", "no_filter", "filter"]

    def prepare_app(self, app, profiler, filters):
        if profiler == "no_filter":
            app = LineProfilerMiddleware(app, stream=StringNoopIO(), async_stream=True)
        elif profiler == "filter":
            app = LineProfilerMiddleware(
                app, filters=filters, stream=StringNoopIO(), async_stream=True
            )
        return TestApp(app)


class FibAppWithFilenameFilterTest(BaseTest):
    def setup(self, filters):
        self.app = self.prepare_app(
            fib_app,
            filters,
            filters=[
                FilenameFilter("apps.py"),
            ],
        )

    def time_index_page(self, *args):
        self.app.get("/")

    def time_n_10(self, *args):
        self.app.get("/10")

    def time_n_20(self, *args):
        self.app.get("/20")


class JinjaAppWithFilenameFilterTest(BaseTest):
    def setup(self, filters):
        self.app = self.prepare_app(
            jinja_app,
            filters,
            filters=[
                FilenameFilter("apps.py"),
            ],
        )

    def time_10_items(self, *args):
        self.app.get("/10")

    def time_100_items(self, *args):
        self.app.get("/20")
