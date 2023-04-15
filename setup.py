from sys import version_info

from Cython.Build import cythonize
from setuptools import Extension, setup

setup(
    ext_package="wsgi_lineprof",
    ext_modules=cythonize(
        [
            Extension(
                "extensions",
                sources=["extensions/extensions.pyx", "extensions/timer.c"],
            )
        ],
        compile_time_env={
            "PY_MAJOR_VERSION": version_info.major,
            "PY_MINOR_VERSION": version_info.minor,
        },
    ),
)
