from codecs import open
from os import path
from warnings import warn

from setuptools import Extension, find_packages, setup


root = path.abspath(path.dirname(__file__))

with open(path.join(root, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

cmdclass = {}
source = "extensions/line_profiler."

try:
    from Cython.Distutils import build_ext
    cmdclass["build_ext"] = build_ext
    source += "pyx"
except ImportError:
    source += "c"
    if not path.exists(path.join(root, source)):
        raise Exception("No Cython installation, no generated C file")
    warn("Could not import Cython, using generated C source code instead")

setup(
    name="wsgi-lineprof",

    version="0.1.0",

    description="WSGI middleware for line-by-line profiling",
    long_description=long_description,

    url="https://github.com/pypa/sampleproject",

    author="https://github.com/ymyzk/wsgi-lineprof",
    author_email="miyazaki.dev@gmail.com",

    license="MIT",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    # classifiers=[
    #     "Development Status :: 3 - Alpha",
    #     "Intended Audience :: Developers",
    #     "License :: OSI Approved :: MIT License",
    #     # that you indicate whether you support Python 2, Python 3 or both.
    #     "Programming Language :: Python :: 2",
    #     "Programming Language :: Python :: 2.7",
    #     "Programming Language :: Python :: 3",
    #     "Programming Language :: Python :: 3.3",
    #     "Programming Language :: Python :: 3.4",
    #     "Programming Language :: Python :: 3.5",
    # ],

    # What does your project relate to?
    # keywords="sample setuptools development",

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["contrib", "docs", "tests"]),

    ext_modules=[
        Extension("_wsgi_lineprof",
                  sources=[source, "extensions/timer.c"])
    ],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip"s
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=["peppercorn"],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "build": ["Cython>=0.24"]
    },
)
