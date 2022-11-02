from Cython.Build import cythonize
from setuptools import Extension, setup


setup(
    ext_package="wsgi_lineprof",
    ext_modules=cythonize([
        Extension("extensions",
                  sources=["extensions/extensions.pyx", "extensions/timer.c"])
    ]),
)
