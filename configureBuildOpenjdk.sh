#!/bin/bash

if [[ -z "$1" ]] ; then
  echo 'Expected single argument, path to boot jdk' >&2
  exit 1
fi

readonly BOOT_JDK="$1"

readonly MILESTONE='fcs'
readonly USER_SUFFIX='tuxjdk'
readonly UPDATE_VERSION='40'
readonly BUILD_NUMBER='01'

unset JAVA_HOME
unset JDK_HOME
unset JRE_HOME
unset _JAVA_OPTIONS

(
  rm -rf 'build' && mkdir 'build' && cd 'build' \
  && bash ../configure \
    --with-zlib=system \
    --with-giflib=system \
    --disable-debug-symbols \
    --disable-zip-debug-info \
    --with-debug-level=release \
    --with-milestone=$MILESTONE \
    --with-update-version=$UPDATE_VERSION \
    --with-user-release-suffix=$USER_SUFFIX \
    --with-build-number=$BUILD_NUMBER \
    --enable-unlimited-crypto \
    --with-boot-jdk="$BOOT_JDK" \
  && make JAVAC_FLAGS=-g images
)
