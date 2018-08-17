from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

from wsgi_lineprof.filters import FilenameFilter, TotalTimeSorter
from wsgi_lineprof.middleware import LineProfilerMiddleware


def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


# Simple WSGI application
def app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    n = 5
    fib_n = fib(n)
    res = "fib(%d) = %d" % (n, fib_n)
    return [res.encode("utf-8")]


# Set up profiler
filters = [
    FilenameFilter("fib.py"),
    TotalTimeSorter(),
]
# write stats every 10 access.
app = LineProfilerMiddleware(app, filters=filters, buffer_size=10)

server = make_server('127.0.0.1', 8000, app)
print("Serving on 127.0.0.1:8000...")
server.serve_forever()
