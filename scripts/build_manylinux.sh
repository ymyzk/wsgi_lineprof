#!/bin/bash
set -ex

cd "$(dirname $0)/.."

# Avoid using PyPy under /opt/python/
for PYBIN in /opt/python/cp*/bin; do
  rm -rf build
  "${PYBIN}/python" -m build --wheel
done

cd dist
for whl in *.whl; do
  # Writes to dist/wheelhouse/
  auditwheel repair "$whl"
  rm "$whl"
done
