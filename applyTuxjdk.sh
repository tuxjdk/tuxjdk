#!/bin/bash

source $(realpath $(dirname ${BASH_SOURCE[0]})/setupQuiltEnv.sh)

echo "Applying quilt patches on current folder..."
quilt push -a
echo "Quilt patches applied."
