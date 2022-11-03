from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults

from wsgi_lineprof.filters import FilenameFilter, TotalTimeSorter
from wsgi_lineprof.middleware import LineProfilerMiddleware


def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


# Simple WSGI application
def app(environ, start_response):
    setup_testing_defaults(environ)

    status = "200 OK"
    headers = [("Content-type", "text/plain; charset=utf-8")]

    start_response(status, headers)

    n = 30
    fib_n = fib(n)
    res = "fib(%d) = %d" % (n, fib_n)
    return [res.encode("utf-8")]


if __name__ == "__main__":
    # Set up profiler
    filters = [
        FilenameFilter("fib.py"),
        TotalTimeSorter(),
    ]
    app = LineProfilerMiddleware(app, filters=filters)

    server = make_server("127.0.0.1", 8000, app)
    print("Serving on 127.0.0.1:8000...")
    server.serve_forever()
