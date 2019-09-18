wsgi_lineprof
=============

**wsgi_lineprof** is a WSGI middleware for line-by-line profiling.

wsgi_lineprof has the following features:

* *WSGI middleware*: It can be integrated with any WSGI-compatible applications and frameworks including Django, Pyramid, Flask, Bottle, and more.
* *Easily pluggable*: All configurations for profiling in one place. Users don't need to make any changes to their application.

wsgi_lineprof is *not recommended to be used in production environment* because of the overhead of profiling.

Contents
--------

.. toctree::
   :maxdepth: 2

   quickstart
   examples
   configuration
   reference
   special-thanks


Links
-----
* `GitHub: ymyzk/wsgi_lineprof <https://github.com/ymyzk/wsgi_lineprof>`_
* `WSGI ミドルウェアとして使えるラインプロファイラを作った話 – ymyzk’s blog <https://blog.ymyzk.com/2016/12/line-profiler-as-a-wsgi-middleware/>`_
* `Python ウェブアプリのためのプロファイラ wsgi_lineprof の仕組み – ymyzk’s blog <https://blog.ymyzk.com/2018/12/how-wsgi-lineprof-works/>`_
* `Python ウェブアプリケーションのためのプロファイラの実装 // Implementation of a profiler for Python web applications - PyCon JP 2019 <https://speakerdeck.com/ymyzk/implementation-of-a-profiler-for-python-web-applications>`_

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
