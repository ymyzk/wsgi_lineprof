Examples
========
TBD

.. Results contain many other functions, you can remove unnecessary results by
.. using *filters*.
.. Example usage with Bottle:
..
.. .. code-block:: python
..
..    import time
..
..    import bottle
..    from wsgi_lineprof.middleware import LineProfilerMiddleware
..
..    app = bottle.default_app()
..
..
..    @app.route('/')
..    def index():
..        time.sleep(1)
..        return "Hello world!!"
..
..    if __name__ == "__main__":
..        # Add wsgi_lineprof as a WSGI middleware!
..        app = LineProfilerMiddleware(app)
..        bottle.run(app=app)
..
.. Run the above script to start web server, then access http://127.0.0.1:8080.
..
.. wsgi_lineprof writes results to stdout every time an HTTP request is processed by default.
.. You can see the output like this in your console:
..
.. ::
..
..    ... (snip) ...
..
..    File: ./app.py
..    Name: index
..    Total time: 1.00518 [sec]
..      Line      Hits         Time  Code
..    ===================================
..         9                         @app.route('/')
..        10                         def index():
..        11         1      1005175      time.sleep(1)
..        12         1            4      return "Hello world!!"
..
..    ... (snip) ...
..
.. Results contain many other functions, you can remove unnecessary results by
.. using *filters*.
