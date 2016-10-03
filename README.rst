wsgi_lineprof
=============

**wsgi_lineprof** is a WSGI middleware for line-by-line profiling.

Please note that this project is under development,
so you may see many API imcompatible changes.

At a Glance
-----------
You can use wsgi_lineprof as a WSGI middleware of existing applications.

::

   $ pip install wsgi_lineprof

Example usage with Bottle:

.. code-block:: python

   import time

   import bottle
   from wsgi_lineprof.middleware import LineProfilerMiddleware

   app = bottle.default_app()


   @app.route('/')
   def index():
       time.sleep(1)
       return "Hello world!!"

   if __name__ == "__main__":
       # Add wsgi_lineprof as a WSGI middleware!
       app = LineProfilerMiddleware(app)
       bottle.run(app=app)

Run the above script to start web server, then access http://127.0.0.1:8080.

You can see the results of profiling functions like this:

::

   File: ./app.py
   Name: index
   Total time: 1.00518 [sec]
     Line      Hits         Time  Code
   ===================================
        9                         @app.route('/')
       10                         def index():
       11         1      1005175      time.sleep(1)
       12         1            4      return "Hello world!!"
