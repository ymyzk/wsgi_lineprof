#!/bin/bash
set -e -x

cd $(dirname $0)
cd ..

for PYBIN in /opt/python/cp3*/bin; do
  rm -rf build
  "${PYBIN}/python" setup.py bdist_wheel
done

cd dist
for whl in *.whl; do
    auditwheel repair "$whl"
    rm "$whl"
done
