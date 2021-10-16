#!/bin/bash
set -e

readonly versions=(
  "python3.6"
  "python3.7"
)
readonly venv="venv-wheel"

cd $(dirname $0)
cd ..

for python in ${versions[@]}; do
  rm -rf build
  rm -rf $venv
  virtualenv -p $python $venv
  . $venv/bin/activate
  pip install -U setuptools pip wheel
  $python setup.py bdist_wheel
  deactivate
done

rm -rf $venv
virtualenv -p python3 $venv
pip install -U setuptools pip wheel
pip install -U delocate
delocate-addplat --rm-orig \
  -p macosx_10_14_x86_64 \
  -p macosx_10_13_x86_64 \
  -p macosx_10_12_x86_64 \
  -p macosx_10_11_x86_64 \
  -p macosx_10_10_x86_64 \
  dist/*.whl
rm -rf $venv
