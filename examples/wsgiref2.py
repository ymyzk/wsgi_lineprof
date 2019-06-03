from wsgiref.simple_server import demo_app, make_server

from wsgi_lineprof.middleware import LineProfilerMiddleware


app = LineProfilerMiddleware(demo_app)

if __name__ == "__main__":
    httpd = make_server('', 8000, app)
    print("Serving HTTP on port 8000...")
    httpd.serve_forever()
