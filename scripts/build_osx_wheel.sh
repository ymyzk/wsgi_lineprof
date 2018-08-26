#!/bin/bash
set -e

readonly versions=(
  "python2.7"
  "python3.4"
  "python3.5"
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
  . venv-wheel/bin/activate
  pip install -U setuptools pip wheel
  $python setup.py bdist_wheel
  deactivate
done

rm -rf $venv
virtualenv -p python3 $venv
pip install -U setuptools pip wheel
pip install -U delocate
delocate-addplat --rm-orig \
  -p macosx-10.12-x86_64 \
  -p macosx-10.11-x86_64 \
  -p macosx-10.10-x86_64 \
  dist/*.whl
rm -rf $venv
