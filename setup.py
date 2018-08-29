from io import open
from os import path
from warnings import warn

from setuptools import Extension, find_packages, setup


root = path.abspath(path.dirname(__file__))

with open(path.join(root, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

source = "extensions/_wsgi_lineprof."

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

    version="0.5.0",

    description="WSGI middleware for line-by-line profiling",
    long_description=long_description,

    url="https://github.com/ymyzk/wsgi_lineprof",

    author="Yusuke Miyazaki",
    author_email="miyazaki.dev@gmail.com",

    license="MIT",

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
    ],

    # What does your project relate to?
    # keywords="sample setuptools development",

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    package_data={
        "wsgi_lineprof": ["py.typed"],
    },

    ext_modules=cythonize([
        Extension("_wsgi_lineprof",
                  sources=[source, "extensions/timer.c"])
    ]),

    install_requires=[
        "six>=1.10.0",
    ],

    extras_require={
        ":python_version < '3.5'": ["typing"],
        "build": ["Cython>=0.28.5,<0.29"],
        "docs": ["Sphinx>=1.4,<1.5"],
        "test": [
            "flake8>=3.0.0,<4.0.0",
            "pytest>=3.0.0,<4.0.0",
        ],
        "test:python_version>='3.0'": [
            "mypy>=0.521,<1.0",
        ]
    },
)
