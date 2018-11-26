import random
import string

from webtest import TestApp

from wsgi_lineprof.filters import FilenameFilter
from wsgi_lineprof.middleware import LineProfilerMiddleware
from .apps import demo_app, fib_app, jinja_app, re_app


class StringNoopIO(object):
    def write(self, _):
        pass


def prepare_app(app, profiler, filters=None):
    if filters is None:
        filters = []

    if profiler == "sync":
        app = LineProfilerMiddleware(app,
                                     filters=filters,
                                     stream=StringNoopIO())
    elif profiler == "async":
        app = LineProfilerMiddleware(app,
                                     filters=filters,
                                     stream=StringNoopIO(),
                                     async_stream=True)
    return TestApp(app)


class DemoAppTest(object):
    param_names = ["profiler"]
    params = ["base", "sync", "async"]

    def setup(self, profiler):
        self.app = prepare_app(demo_app, profiler)

    def time_index_page(self, *args):
        self.app.get("/")


class FibAppTest(object):
    param_names = ["profiler"]
    params = ["base", "sync", "async"]

    def setup(self, profiler):
        self.app = prepare_app(fib_app, profiler)

    def time_index_page(self, *args):
        self.app.get("/")

    def time_n_10(self, *args):
        self.app.get("/10")

    def time_n_20(self, *args):
        self.app.get("/20")


class FibAppWithFilenameFilterTest(object):
    param_names = ["profiler"]
    params = ["base", "sync", "async"]

    def setup(self, profiler):
        filters = [
            FilenameFilter("apps.py"),
        ]
        self.app = prepare_app(fib_app, profiler, filters=filters)

    def time_index_page(self, *args):
        self.app.get("/")

    def time_n_10(self, *args):
        self.app.get("/10")

    def time_n_20(self, *args):
        self.app.get("/20")


class JinjaAppTest(object):
    param_names = ["profiler"]
    params = ["base", "sync", "async"]

    def setup(self, profiler):
        self.app = prepare_app(jinja_app, profiler)

    def time_10_items(self, *args):
        self.app.get("/10")

    def time_100_items(self, *args):
        self.app.get("/20")


class JinjaAppWithFilenameFilterTest(object):
    param_names = ["profiler"]
    params = ["base", "sync", "async"]

    def setup(self, profiler):
        filters = [
            FilenameFilter("apps.py"),
        ]
        self.app = prepare_app(jinja_app, profiler, filters=filters)

    def time_10_items(self, *args):
        self.app.get("/10")

    def time_100_items(self, *args):
        self.app.get("/20")


class ReAppTest(object):
    param_names = ["profiler"]
    params = ["base", "sync", "async"]

    def setup(self, profiler):
        self.app = prepare_app(re_app, profiler)
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        random.seed(12345)
        random_str = "".join(random.choice(chars) for _ in range(2000))
        self.random_str = "/" + random_str
        random.seed()

    def time_index_page(self, *args):
        self.app.get("/")

    def time_email_address(self, *args):
        self.app.get("/EMAIL-address-8324236rq@example.com")

    def time_ip_address(self, *args):
        self.app.get("/ip-address-is-123.21.13.149")

    def time_random(self, *args):
        self.app.get(self.random_str)
