"""Benchmarks with different stream writers

base: Application without LineProfilerMiddleware
sync: Application with LineProfilerMiddleware using SyncWriter
async: Application with LineProfilerMiddleware using AsyncWriter
"""

import random
import string

from webtest import TestApp

from wsgi_lineprof.middleware import LineProfilerMiddleware

from .apps import demo_app, fib_app, jinja_app, re_app
from .utils import StringNoopIO


class BaseTest:
    param_names = ["writer"]
    params = ["base", "sync", "async"]

    def prepare_app(self, app, writer):
        if writer == "sync":
            app = LineProfilerMiddleware(app, stream=StringNoopIO())
        elif writer == "async":
            app = LineProfilerMiddleware(app, stream=StringNoopIO(), async_stream=True)
        return TestApp(app)


class DemoAppTest(BaseTest):
    def setup(self, writer):
        self.app = self.prepare_app(demo_app, writer)

    def time_index_page(self, *args):
        self.app.get("/")


class FibAppTest(BaseTest):
    def setup(self, writer):
        self.app = self.prepare_app(fib_app, writer)

    def time_index_page(self, *args):
        self.app.get("/")

    def time_n_10(self, *args):
        self.app.get("/10")

    def time_n_20(self, *args):
        self.app.get("/20")


class JinjaAppTest(BaseTest):
    def setup(self, writer):
        self.app = self.prepare_app(jinja_app, writer)

    def time_10_items(self, *args):
        self.app.get("/10")

    def time_100_items(self, *args):
        self.app.get("/20")


class ReAppTest(BaseTest):
    def setup(self, writer):
        self.app = self.prepare_app(re_app, writer)
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
