from __future__ import print_function
import re
import sys
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults

import jinja2
from six import StringIO

from wsgi_lineprof.middleware import LineProfilerMiddleware


RE_IP = (
    r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
    r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
)
RE_EMAIL = (
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*"
    r"|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@[0-9A-Za-z]"
    r"([0-9A-Za-z-]{0,61}[0-9A-Za-z])?"
    r"(\.[0-9A-Za-z]([0-9A-Za-z-]{0,61}[0-9A-Za-z])?)+"
)
JINJA_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <title>{{ title }}</title>
</head>
<body>
  <h1>{{ title }}</h1>
  <ul>
  {% for user in users %}
    <li>
      <a href="/users/{{ user.url }}">{{ user.name }}</a>
      {% if loop.index is divisibleby 2 %}Active{% else %}Inactive{% endif %}
    </li>
  {% endfor %}
  </ul>
</body>
</html>"""


def demo_app(environ, start_response):
    """Copy of wsgiref.simple_server.demo_app"""
    stdout = StringIO()
    print("Hello world!", file=stdout)
    print(file=stdout)
    h = sorted(environ.items())
    for k, v in h:
        print(k, '=', repr(v), file=stdout)
    start_response("200 OK", [('Content-Type', 'text/plain; charset=utf-8')])
    return [stdout.getvalue().encode("utf-8")]


def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def fib_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    m = re.match(r"/([1-9][0-9]*)", environ["PATH_INFO"])
    if m:
        n = int(m.group(1))
    else:
        n = 5

    fib_n = fib(n)
    res = "fib(%d) = %d" % (n, fib_n)
    return [res.encode("utf-8")]


def re_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    text = environ["PATH_INFO"]

    res = ""

    re.match(RE_EMAIL, text)
    res += str(re.search(RE_EMAIL, text))
    res += "\n"

    re.match(RE_IP, text)
    res += str(re.search(RE_IP, text))
    res += "\n"

    return [res.encode("utf-8")]


def jinja_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]

    start_response(status, headers)

    m = re.match(r"/([1-9][0-9]*)", environ["PATH_INFO"])
    if m:
        n = int(m.group(1))
    else:
        n = 5

    template = jinja2.Template(JINJA_TEMPLATE)
    users = [{"url": str(i), "name": "A" * i} for i in range(n)]
    res = template.render(title="Benchmark", users=users)
    return [res.encode("utf-8")]


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.exit(1)

    app_name = sys.argv[1]
    if not app_name.endswith("_app"):
        sys.exit(1)
    app = locals()[app_name]
    # Set up profiler
    app = LineProfilerMiddleware(app)

    server = make_server('127.0.0.1', 8000, app)
    print("Serving on 127.0.0.1:8000...")
    server.serve_forever()
