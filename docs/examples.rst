Examples
========

wsgiref (Python 2)
------------------
An example of using wsgi_lineprof with `wsgiref for Python 2 <https://docs.python.org/2.7/library/wsgiref.html>`_.

.. code-block:: python

   from wsgiref.simple_server import demo_app, make_server

   from wsgi_lineprof.middleware import LineProfilerMiddleware


   app = LineProfilerMiddleware(demo_app)

   if __name__ == "__main__":
       httpd = make_server('', 8000, app)
       print("Serving HTTP on port 8000...")
       httpd.serve_forever()

wsgiref (Python 3)
------------------
An example of using wsgi_lineprof with `wsgiref for Python 3 <https://docs.python.org/3/library/wsgiref.html>`_.

.. code-block:: python

   from wsgiref.simple_server import demo_app, make_server

   from wsgi_lineprof.middleware import LineProfilerMiddleware


   app = LineProfilerMiddleware(demo_app)

   if __name__ == "__main__":
       with make_server('', 8000, app) as httpd:
           print("Serving HTTP on port 8000...")
           httpd.serve_forever()

Bottle
------
Examples of using wsgi_lineprof with `Bottle <https://bottlepy.org/>`_.

.. code-block:: python

   import bottle

   from wsgi_lineprof.middleware import LineProfilerMiddleware


   @bottle.route('/hello/<name>')
   def index(name):
       return bottle.template('<b>Hello {{name}}</b>!', name=name)

   app = LineProfilerMiddleware(bottle.app())

   if __name__ == "__main__":
       bottle.run(host='localhost', port=8080, app=app)

.. code-block:: python

   import bottle

   from wsgi_lineprof.middleware import LineProfilerMiddleware


   app = bottle.app()

   @app.route('/hello/<name>')
   def index(name):
       return bottle.template('<b>Hello {{name}}</b>!', name=name)

   app = LineProfilerMiddleware(app)

   if __name__ == "__main__":
       bottle.run(host='localhost', port=8080, app=app)
