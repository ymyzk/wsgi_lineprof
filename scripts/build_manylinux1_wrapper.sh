#!/bin/bash
set -e

cd $(dirname $0)
cd ..

docker run --rm -v `pwd`:/app quay.io/pypa/manylinux1_x86_64 /app/scripts/build_manylinux1.sh
docker run --rm -v `pwd`:/app quay.io/pypa/manylinux1_i686 linux32 /app/scripts/build_manylinux1.sh
