Examples
========

wsgiref
-------
An example of using wsgi_lineprof with `wsgiref <https://docs.python.org/3/library/wsgiref.html>`_.

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

Flask
-----
An example of using wsgi_lineprof with `Flask <https://github.com/pallets/flask>`_.

.. code-block:: python

   from flask import Flask
   from wsgi_lineprof.middleware import LineProfilerMiddleware

   app = Flask(__name__)

   @app.route("/")
   def hello():
       return "Hello, World!"

   app.wsgi_app = LineProfilerMiddleware(app.wsgi_app)

   if __name__ == '__main__':
       app.run(port=8000)

Django
------
An example of using wsgi_lineprof with `Django <https://www.djangoproject.com>`_.
We can load wsgi_lineprof in ``<YOUR_PROJECT>.wsgi.py``.

.. code-block:: python

   import os

   from django.core.wsgi import get_wsgi_application
   from wsgi_lineprof.middleware import LineProfilerMiddleware

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<YOUR_PROJECT>.settings')

   application = get_wsgi_application()
   application = LineProfilerMiddleware(application)
