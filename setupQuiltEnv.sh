#!/bin/bash

QUILT="$( which quilt 2>/dev/null )"
if [[ -z $QUILT ]] ; then
  echo 'quilt not found' >&2
  exit 1
fi

printQuiltPatchesDir() {
  local SCRIPT_SOURCE
  local SCRIPT_DIR
  local QUILT_PATCHES
  ## resolve folder of this script, following all symlinks,
  ## http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
  SCRIPT_SOURCE="${BASH_SOURCE[0]}"
  while [ -h "$SCRIPT_SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
    SCRIPT_DIR="$( cd -P "$( dirname "$SCRIPT_SOURCE" )" && pwd )"
    SCRIPT_SOURCE="$(readlink "$SCRIPT_SOURCE")"
    # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    [[ $SCRIPT_SOURCE != /* ]] && SCRIPT_SOURCE="$SCRIPT_DIR/$SCRIPT_SOURCE"
  done
  SCRIPT_DIR="$( cd -P "$( dirname "$SCRIPT_SOURCE" )" && pwd )"
  QUILT_PATCHES="$SCRIPT_DIR/quilt-patches"
  echo "$QUILT_PATCHES"
}

QUILT_PATCHES="$( printQuiltPatchesDir )"
echo "setting QUILT_PATCHES variable to: $QUILT_PATCHES"
export QUILT_PATCHES

EDITOR='nano'
echo "setting EDITOR to: $EDITOR"
export EDITOR
