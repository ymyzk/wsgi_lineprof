import bottle

from wsgi_lineprof.middleware import LineProfilerMiddleware


@bottle.route("/hello/<name>")
def index(name):
    return bottle.template("<b>Hello {{name}}</b>!", name=name)


app = LineProfilerMiddleware(bottle.app())

if __name__ == "__main__":
    bottle.run(host="localhost", port=8080, app=app)
