#!/bin/bash
set -e

cd "$(dirname $0)/.."

# See https://github.com/pypa/manylinux

# For this project,
# manylinux_2_24_x86_64 can build manylinux2014_x86_64/manylinux_2_17_x86_64 as well
# manylinux2010_x86_64 can build manylinux1_x86_64/manylinux_2_5_x86_64 as well
readonly images=(manylinux_2_24_x86_64 manylinux_2_24_i686 manylinux2010_x86_64 manylinux2010_i686)

for image in "${images[@]}"; do
  full_image="quay.io/pypa/$image"
  docker pull "$full_image"
  docker run --rm -v "$(pwd):/app" "$full_image" /app/scripts/build_manylinux.sh
done
