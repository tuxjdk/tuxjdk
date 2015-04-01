#!/bin/bash

QUILT_PATCHES=$(realpath $(dirname ${BASH_SOURCE[0]})/quilt-patches)
echo "setting QUILT_PATCHES variable to: $QUILT_PATCHES"
export QUILT_PATCHES

EDITOR=kwrite
echo "setting EDITOR to: $EDITOR"
export EDITOR
