#!/bin/bash

if [[ -n "$1" ]] ; then
  readonly BOOT_JDK="$1"
else
  echo 'Boot jdk argument was not privded, trying to guess...'
  if [ -x '/opt/tuxjdk/tuxjdk/bin/javac' ] ; then
    readonly BOOT_JDK='/opt/tuxjdk/tuxjdk'
  elif [ -x '/usr/lib/jvm/java/bin/javac' ] ; then
    readonly BOOT_JDK='/usr/lib/jvm/java'
  elif [ -x '/usr/lib64/jvm/java/bin/javac' ] ; then
    readonly BOOT_JDK='/usr/lib64/jvm/java'
  else
    echo 'Could not guess the bootjdk location, exiting.' >&2
    exit 1
  fi
  echo "Using boot jdk: '$BOOT_JDK'"
fi

readonly MILESTONE='fcs'
readonly USER_SUFFIX='tuxjdk'
readonly PRODUCT_NAME='TuxJdk'
readonly UPDATE_VERSION='60'
readonly BUILD_NUMBER='03'

unset JAVA_HOME
unset JDK_HOME
unset JRE_HOME
unset _JAVA_OPTIONS

## jdk8u45 still does not support linux 4.0 officially,
## so we have to disable os version check because
## tumbleweed already has 4.0-based kernel:
export DISABLE_HOTSPOT_OS_VERSION_CHECK=ok

(
  rm -rf 'build' && mkdir 'build' && cd 'build' \
  && bash ../configure \
    --with-zlib=system \
    --with-giflib=system \
    --disable-debug-symbols \
    --disable-zip-debug-info \
    --with-debug-level=release \
    --with-stdc++lib=dynamic \
    --with-milestone=$MILESTONE \
    --with-update-version=$UPDATE_VERSION \
    --with-user-release-suffix=$USER_SUFFIX \
    --with-build-number=$BUILD_NUMBER \
    --enable-unlimited-crypto \
    --with-boot-jdk="$BOOT_JDK" \
  && make \
    JAVAC_FLAGS=-g \
    COMPRESS_JARS=true \
    LAUNCHER_NAME=$USER_SUFFIX \
    PRODUCT_NAME=$PRODUCT_NAME \
    JDK_UPDATE_VERSION=$UPDATE_VERSION \
    HOTSPOT_VM_DISTRO=$PRODUCT_NAME \
    HOTSPOT_BUILD_VERSION=tuxjdk-$BUILD_NUMBER \
    images
)
