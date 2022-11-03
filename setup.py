from setuptools import Extension, setup

setup(
    ext_package="wsgi_lineprof",
    ext_modules=[
        Extension(
            # setuptools should discover Cython automatically
            "extensions",
            sources=["extensions/extensions.pyx", "extensions/timer.c"],
        )
    ],
)
