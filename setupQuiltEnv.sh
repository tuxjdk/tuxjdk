#!/bin/bash

readonly QUILT="$( which quilt 2>/dev/null )"
if [[ -z $QUILT ]] ; then
  echo 'quilt not found' >&2
  exit 1
fi

## resolve folder of this script, following all symlinks,
## http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
SCRIPT_SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SCRIPT_SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  SCRIPT_DIR="$( cd -P "$( dirname "$SCRIPT_SOURCE" )" && pwd )"
  SCRIPT_SOURCE="$(readlink "$SCRIPT_SOURCE")"
  # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
  [[ $SCRIPT_SOURCE != /* ]] && SCRIPT_SOURCE="$SCRIPT_DIR/$SCRIPT_SOURCE"
done
readonly SCRIPT_DIR="$( cd -P "$( dirname "$SCRIPT_SOURCE" )" && pwd )"
readonly QUILT_PATCHES="$SCRIPT_DIR/quilt-patches"

echo "setting QUILT_PATCHES variable to: $QUILT_PATCHES"
export QUILT_PATCHES

readonly EDITOR='kwrite'
echo "setting EDITOR to: $EDITOR"
export EDITOR
