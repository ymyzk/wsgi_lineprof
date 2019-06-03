wsgi_lineprof
=============
.. image:: https://badge.fury.io/py/wsgi-lineprof.svg
   :target: https://pypi.python.org/pypi/wsgi-lineprof/
   :alt: PyPI version
.. image:: https://img.shields.io/pypi/pyversions/wsgi_lineprof.svg
   :target: https://pypi.python.org/pypi/wsgi-lineprof/
   :alt: PyPI Supported Python Versions
.. image:: https://travis-ci.org/ymyzk/wsgi_lineprof.svg?branch=master
   :target: https://travis-ci.org/ymyzk/wsgi_lineprof
   :alt: Build Status
.. image:: https://ci.appveyor.com/api/projects/status/cjhft69q2hq1gdoj?svg=true
   :target: https://ci.appveyor.com/project/ymyzk/wsgi-lineprof
   :alt: AppVeyor Build Status
.. image:: https://readthedocs.org/projects/wsgi_lineprof/badge/?version=latest
   :target: https://wsgi_lineprof.readthedocs.io/
   :alt: Documentation Status

**wsgi_lineprof** is a WSGI middleware for line-by-line profiling.

wsgi_lineprof has the following features:

* *WSGI middleware*: It can be integrated with any WSGI-compatible applications and frameworks including Django, Pyramid, Flask, Bottle, and more.
* *Easily pluggable*: All configurations for profiling in one place. Users don't need to make any changes to their application.

wsgi_lineprof is *not recommended to be used in production environment* because of the overhead of profiling.

At a Glance
-----------
You can use wsgi_lineprof as a WSGI middleware of existing applications.

::

   $ pip install wsgi_lineprof

Apply wsgi_lineprof to the existing WSGI web application:

.. code-block:: python

   from wsgi_lineprof.middleware import LineProfilerMiddleware
   app = LineProfilerMiddleware(app)

Start the web application and access to the application.
wsgi_lineprof writes results to stdout every time an HTTP request is processed by default.
You can see the output like this in your console:

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

Please check `the documentation <https://wsgi-lineprof.readthedocs.io/en/latest/index.html>`_ for more details.
