.. wsgi_lineprof documentation master file, created by
   sphinx-quickstart on Fri May 24 14:07:35 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

wsgi_lineprof
=============

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

Results contain many other functions, you can remove unnecessary results by
using *filters*.

Contents
--------

.. toctree::
   :maxdepth: 2

   usage
   reference


Links
-----
* `GitHub: ymyzk/wsgi_lineprof <https://github.com/ymyzk/wsgi_lineprof>`_
* `WSGI ミドルウェアとして使えるラインプロファイラを作った話 – ymyzk’s blog <https://blog.ymyzk.com/2016/12/line-profiler-as-a-wsgi-middleware/>`_
* `Python ウェブアプリのためのプロファイラ wsgi_lineprof の仕組み – ymyzk’s blog <https://blog.ymyzk.com/2018/12/how-wsgi-lineprof-works/>`_

Special Thanks
^^^^^^^^^^^^^^
This project uses code from the following project:

* `rkern/line_profiler <https://github.com/rkern/line_profiler>`_

This project is inspired by the following project:

* `kainosnoema/rack-lineprof <https://github.com/kainosnoema/rack-lineprof>`_

wsgi_lineprof is integrated with the following projects:

* `kobinpy/wsgicli <https://github.com/kobinpy/wsgicli>`_
* `denzow/wsgi_lineprof_reporter <https://github.com/denzow/wsgi_lineprof_reporter>`_

wsgi_lineprof is mentioned in the following entries:

* `1日目 Peter Wang氏キーノート，変数アノテーション，自然言語処理，PythonでWebセキュリティ自動化～新企画「メディア会議」に注目：PyCon JP 2017カンファレンスレポート｜gihyo.jp … 技術評論社 <http://gihyo.jp/news/report/01/pyconjp2017/0001?page=4>`_
* `DjangoにDjangoミドルウェアとWSGIミドルウェアを組み込んでみた - メモ的な思考的な <http://thinkami.hatenablog.com/entry/2016/12/13/061856>`_
* `PythonのWSGIラインプロファイラを試してみた(wsgi_lineprof) - [Dd]enzow(ill)? with DB and Python <http://www.denzow.me/entry/2017/09/18/162154>`_
* `PythonのWSGIラインプロファイラの結果を使いやすくしてみた(wsgi_lineprof_reporter) - [Dd]enzow(ill)? with DB and Python <http://www.denzow.me/entry/2017/09/20/233219>`_
* `Server-side development — c2cgeoportal documentation <https://camptocamp.github.io/c2cgeoportal/master/developer/server_side.html>`_

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
