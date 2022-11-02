#!/bin/bash
set -ex

cd "$(dirname $0)/.."

# Avoid using PyPy under /opt/python/
for PYBIN in /opt/python/cp*/bin; do
  rm -rf build
  if [[ "$PYBIN" == /opt/python/cp36-* ]]; then
    echo "Skipping Python 3.6 as we already stopped supporting it".
    continue
  fi
  if [[ "$PYBIN" == /opt/python/cp311-* ]]; then
    echo "Skipping Python 3.11 until we fully support it."
    continue
  fi
  "${PYBIN}/python" -m build --wheel
done

cd dist
for whl in *.whl; do
  # Writes to dist/wheelhouse/
  auditwheel repair "$whl"
  rm "$whl"
done
