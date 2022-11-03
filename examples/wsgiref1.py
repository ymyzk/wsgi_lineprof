from wsgiref.simple_server import demo_app, make_server

from wsgi_lineprof.middleware import LineProfilerMiddleware

app = LineProfilerMiddleware(demo_app)

if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving HTTP on port 8000...")
        httpd.serve_forever()
