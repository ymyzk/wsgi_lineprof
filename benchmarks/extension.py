"""Benchmarks with different line profilers

base: Application without LineProfiler
noop: Application with NoopLineProfiler
enabled: Application with LineProfiler
"""

import random
import string

from webtest import TestApp

from wsgi_lineprof.extensions import LineProfiler

from .apps import demo_app, fib_app, jinja_app, re_app


class NoopLineProfiler(LineProfiler):
    def enable(self):
        self._enable_noop()


class Middleware:
    def __init__(self, app, profiler_class):
        self.app = app
        self.profiler_class = profiler_class

    def __call__(self, env, start_response):
        profiler = self.profiler_class()
        profiler.enable()
        try:
            response = self.app(env, start_response)
        finally:
            profiler.disable()
        return response


class BaseTest:
    param_names = ["profiler"]
    params = ["base", "noop", "enabled"]

    def prepare_app(self, app, profiler):
        if profiler == "noop":
            app = Middleware(app, profiler_class=NoopLineProfiler)
        elif profiler == "enabled":
            app = Middleware(app, profiler_class=LineProfiler)
        return TestApp(app)


class DemoAppTest(BaseTest):
    def setup(self, profiler):
        self.app = self.prepare_app(demo_app, profiler)

    def time_index_page(self, *args):
        self.app.get("/")


class FibAppTest(BaseTest):
    def setup(self, profiler):
        self.app = self.prepare_app(fib_app, profiler)

    def time_index_page(self, *args):
        self.app.get("/")

    def time_n_10(self, *args):
        self.app.get("/10")

    def time_n_20(self, *args):
        self.app.get("/20")


class JinjaAppTest(BaseTest):
    def setup(self, profiler):
        self.app = self.prepare_app(jinja_app, profiler)

    def time_10_items(self, *args):
        self.app.get("/10")

    def time_100_items(self, *args):
        self.app.get("/20")


class ReAppTest(BaseTest):
    def setup(self, profiler):
        self.app = self.prepare_app(re_app, profiler)
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
