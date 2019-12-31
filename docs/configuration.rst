Configuration
=============
This page describes configuration options of wsgi_lineprof.
You can provide various options as keyword arguments to change the behavior of the profiler:

.. code-block:: python

    from wsgi_lineprof.middleware import LineProfilerMiddleware
    app = LineProfilerMiddleware(app, **options)

Filters
-------
Users can get results from specific files or sort results by using filters.
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

There are more useful filters in ``wsgi_lineprof.filters``. Examples:

* ``FilenameFilter("(file1|file2).py", regex=True)``
* ``NameFilter("(fun1|fun2).py", regex=True)``

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

Accumulate Mode
---------------
By default, wsgi_lineprof writes results every time a request is processed.
By enabling ``accumulate`` option, wsgi_lineprof accumulate results of all requests and writes the result on interpreter termination.

.. code-block:: python

    app = LineProfilerMiddleware(app, accumulate=True)
    bottle.run(app=app)

Colorize Output
---------------
Colorized output is enabled by default for stdout and stderr.
You can disable the feature using the ``color`` option.

.. code-block:: python

    app = LineProfilerMiddleware(app, color=False)
    bottle.run(app=app)

Result Endpoint
---------------
By default, you can access an endpoint ``/wsgi_lineprof/`` to see the results.
This endpoint is configurable.

.. code-block:: python

    app = LineProfilerMiddleware(app, endpoint='/custom_result_endpoint/')
    bottle.run(app=app)
