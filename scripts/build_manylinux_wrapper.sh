#!/bin/bash
set -e

cd $(dirname $0)
cd ..

docker pull quay.io/pypa/manylinux2010_x86_64
docker pull quay.io/pypa/manylinux1_x86_64
docker pull quay.io/pypa/manylinux1_i686

# manylinux2010 image also produces wheel for manylinux1
# but we override them using wheel produced by manulinux1 image later
docker run --rm -v `pwd`:/app quay.io/pypa/manylinux2010_x86_64 /app/scripts/build_manylinux.sh
docker run --rm -v `pwd`:/app quay.io/pypa/manylinux1_x86_64 /app/scripts/build_manylinux.sh
docker run --rm -v `pwd`:/app quay.io/pypa/manylinux1_i686 linux32 /app/scripts/build_manylinux.sh
