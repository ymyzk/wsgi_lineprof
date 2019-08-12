from io import open
from os import path
from warnings import warn

from setuptools import Extension, setup


root = path.abspath(path.dirname(__file__))

with open(path.join(root, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

source = "extensions/extensions."

try:
    from Cython.Build import cythonize
    source += "pyx"
except ImportError:
    def cythonize(extensions):
        return extensions
    source += "c"
    if not path.exists(path.join(root, source)):
        raise Exception("No Cython installation, no generated C file")
    warn("Could not import Cython, using generated C source code instead")

setup(
    name="wsgi_lineprof",

    version="0.8.0",

    description="WSGI middleware for line-by-line profiling",
    long_description=long_description,

    url="https://github.com/ymyzk/wsgi_lineprof",

    author="Yusuke Miyazaki",
    author_email="miyazaki.dev@gmail.com",

    license="MIT",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: C",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Software Development",
        "Topic :: System :: Benchmark",
    ],

    # What does your project relate to?
    # keywords="sample setuptools development",

    packages=[
        "wsgi_lineprof",
    ],
    package_data={
        "wsgi_lineprof": ["py.typed", "*.pyi"],
    },

    ext_package="wsgi_lineprof",
    ext_modules=cythonize([
        Extension("extensions",
                  sources=[source, "extensions/timer.c"])
    ]),

    install_requires=[
        "six>=1.10.0",
    ],

    extras_require={
        ":python_version < '3.5'": ["typing"],
        "benchmark": [
            "asv>=0.3.1,<0.4",
            "virtualenv",
        ],
        "benchmark-deps": [
            "Jinja2==2.10",
            "WebTest==2.0.32",
        ],
        "build": ["Cython>=0.28,<0.30"],
        "docs": [
            "Sphinx>=2.1,<2.2",
            "sphinx_rtd_theme>=0.4.3,<0.5",
        ],
        "test": [
            "codecov>=2.0.15,<3.0.0",
            "flake8>=3.0.0,<4.0.0",
            "pytest-cov>=2.6.0,<3.0.0",
        ],
        "test:python_version>='3.0'": [
            "mypy>=0.650,<1.0",
        ],
        "test:python_version<'3.5'": [
            "pytest>=4.0.0,<5.0.0",
        ],
        "test:python_version>='3.5'": [
            "pytest>=5.0.0,<6.0.0",
        ],
    },

    project_urls={
        "Bug Reports": "https://github.com/ymyzk/wsgi_lineprof/issues",
        "Source": "https://github.com/ymyzk/wsgi_lineprof",
    },
)
