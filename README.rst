wsgi_lineprof
=============
.. image:: https://badge.fury.io/py/wsgi-lineprof.svg
   :target: https://pypi.python.org/pypi/wsgi-lineprof/
   :alt: PyPI version
.. image:: https://travis-ci.org/ymyzk/wsgi_lineprof.svg?branch=master
   :target: https://travis-ci.org/ymyzk/wsgi_lineprof
   :alt: Build Status

**wsgi_lineprof** is a WSGI middleware for line-by-line profiling.

wsgi_lineprof shows results of line-by-line profiling per request.
You can use this project with many WSGI-compatible applications and frameworks:

* Django
* Pyramid
* Flask
* Bottle
* etc...

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

The results are outputted to stdout by default.
You can see the results like this:

::

   ... (snip) ...

   File: ./app.py
   Name: index
   Total time: 1.00518 [sec]
     Line      Hits         Time  Code
   ===================================
        9                         @app.route('/')
       10                         def index():
       11         1      1005175      time.sleep(1)
       12         1            4      return "Hello world!!"

   ... (snip) ...

Results contain many other functions, you can remove unnecessary results by
using *filters*.

Requirements
------------
* Python 2.7
* Python 3.4
* Python 3.5
* Python 3.6
* Python 3.7

Filters
-------
You can get results from specific files or sort results by using filters.
For example, use ``FilenameFilter`` to filter results with ``filename``
and use ``TotalTimeSorter`` to sort results by ``total_time``.

.. code-block:: python

    import time

    import bottle
    from wsgi_lineprof.filters import FilenameFilter, TotalTimeSorter
    from wsgi_lineprof.middleware import LineProfilerMiddleware

    app = bottle.default_app()


    def get_name():
        # Get some data...
        time.sleep(1)
        return "Monty Python"

    @app.route('/')
    def index():
        name = get_name()
        return "Hello, {}!!".format(name)

    if __name__ == "__main__":
        filters = [
            # Results which filename contains "app2.py"
            FilenameFilter("app2.py"),
            # Sort by total time of results
            TotalTimeSorter(),
        ]
        # Add wsgi_lineprof as a WSGI middleware
        app = LineProfilerMiddleware(app, filters=filters)

        bottle.run(app=app)

Run the above script to start web server, then access http://127.0.0.1:8080.
You can see results in stdout.

::

    $ ./app2.py
    Bottle v0.12.10 server starting up (using WSGIRefServer())...
    Listening on http://127.0.0.1:8080/
    Hit Ctrl-C to quit.

    Time unit: 1e-06 [sec]

    File: ./app2.py
    Name: index
    Total time: 1.00526 [sec]
      Line      Hits         Time  Code
    ===================================
        15                         @app.route('/')
        16                         def index():
        17         1      1005250      name = get_name()
        18         1           11      return "Hello, {}!!".format(name)

    File: ./app2.py
    Name: get_name
    Total time: 1.00523 [sec]
      Line      Hits         Time  Code
    ===================================
        10                         def get_name():
        11                             # Get some data...
        12         1      1005226      time.sleep(1)
        13         1            4      return "Monty Python"

    127.0.0.1 - - [30/Nov/2016 17:21:12] "GET / HTTP/1.1" 200 21

There are some useful filters in ``wsgi_lineprof.filters``.

Stream
------
By using ``stream`` option, you can output results to a file.
For example, you can output logs to ``lineprof.log``.

.. code-block:: python

    f = open("lineprof.log", "w")
    app = LineProfilerMiddleware(app, stream=f)
    bottle.run(app=app)

Async Stream
------------
By using ``async_stream`` option, wsgi_lineprof starts a new thread for writing results.
This option is useful when you do not want the main thread blocked for writing results.

.. code-block:: python

    # Start a new thread for writing results
    app = LineProfilerMiddleware(app, async_stream=True)
    bottle.run(app=app)

Links
-----
* `GitHub: ymyzk/wsgi_lineprof <https://github.com/ymyzk/wsgi_lineprof>`_
* `WSGI ミドルウェアとして使えるラインプロファイラを作った話 – ymyzk’s blog <https://blog.ymyzk.com/2016/12/line-profiler-as-a-wsgi-middleware/>`_

Special Thanks
^^^^^^^^^^^^^^
This project uses code from the following projects:

* `kainosnoema/rack-lineprof <https://github.com/kainosnoema/rack-lineprof>`_

This project is inspired by the following projects:

* `rkern/line_profiler <https://github.com/rkern/line_profiler>`_

wsgi_lineprof is integrated with the following projects:

* `kobinpy/wsgicli <https://github.com/kobinpy/wsgicli>`_
