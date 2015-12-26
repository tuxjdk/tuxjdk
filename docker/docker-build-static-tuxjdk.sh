#!/bin/bash

set -x
set -e
set -o pipefail

if [ -x '/opt/jdk/bin/javac' ] ; then
  readonly BOOT_JDK='/opt/jdk'
elif [ -x '/usr/lib64/jvm/java/bin/javac' ] ; then
  readonly BOOT_JDK='/usr/lib64/jvm/java'
else
  echo 'No boot jdk found' >&2
  exit 1
fi

readonly MILESTONE='fcs'
readonly USER_SUFFIX='tuxjdk'
readonly PRODUCT_NAME='TuxJdk'
readonly UPDATE_VERSION='66'
readonly BUILD_NUMBER='03'

unset JAVA_HOME
unset JDK_HOME
unset JRE_HOME
unset _JAVA_OPTIONS

cd /tuxjdk

if [[ $( ls -l tuxjdk*.tar.xz | wc -l ) -ne 1 ]] ; then
  echo "Found more than one tuxjdk tarball, exactly one expected: $( ls tuxjdk* )" >&2
  exit 1
fi

if [[ $( ls -l jdk*.tar.xz | wc -l ) -ne 1 ]] ; then
  echo "Found more than one jdk tarball, exactly one expected: $( ls jdk* )" >&2
  exit 1
fi

rm -rf build && mkdir build && cd build
( mkdir tuxjdk && cd tuxjdk && tar --strip-components=1 -xJf /tuxjdk/tuxjdk*.tar.xz )
( mkdir jdk && cd jdk && tar --strip-components=1 -xJf /tuxjdk/jdk*.tar.xz && bash ../tuxjdk/applyTuxjdk.sh && bash ./common/autoconf/autogen.sh)
(
  mkdir building
  cd building
  ## using gcc5 from Leap 42.1:
  export CC=gcc-5
  export CXX=g++-5
  ## jdk8u45 still does not support linux 4.0 officially,
  ## so we have to disable os version check because
  ## tumbleweed already has 4.0-based kernel:
  export DISABLE_HOTSPOT_OS_VERSION_CHECK=ok
  bash /tuxjdk/build/jdk/configure \
    --disable-debug-symbols \
    --disable-zip-debug-info \
    --with-debug-level=release \
    --with-stdc++lib=static \
    --with-milestone=$MILESTONE \
    --with-update-version=$UPDATE_VERSION \
    --with-user-release-suffix=$USER_SUFFIX \
    --with-build-number=$BUILD_NUMBER \
    --enable-unlimited-crypto \
    --with-boot-jdk="$BOOT_JDK"
  make \
    JAVAC_FLAGS=-g \
    LAUNCHER_NAME=$USER_SUFFIX \
    PRODUCT_NAME=$PRODUCT_NAME \
    JDK_UPDATE_VERSION=$UPDATE_VERSION \
    HOTSPOT_VM_DISTRO=$PRODUCT_NAME \
    HOTSPOT_BUILD_VERSION=tuxjdk-$BUILD_NUMBER \
    images
)
# default antialiasing and font size:
( cd building/images/j2sdk-image/jre/lib && : >swing.properties && echo 'ui.defaultFont.size=9' >>swing.properties && echo 'ui.defaultFont.antialiasing=lcd' >>swing.properties )
# certificates:
( cd building/images/j2sdk-image/jre/lib/security && mv cacerts cacerts.orig && cp /var/lib/ca-certificates/java-cacerts ./cacerts )
# deleting samples and demos:
( cd building/images/j2sdk-image && rm -rf 'demo' 'sample' )
# fix permissions for files and dirs:
( cd building/images/j2sdk-image && chmod -R a-w . && chmod -R a+r . && find "$(pwd)" -type d -exec chmod a+x {} + && chmod a+x bin/* && chmod a+x jre/bin/* )
# packing:
OUTPUT="tuxjdk-static-8.${UPDATE_VERSION}.${BUILD_NUMBER}"
if [[ -d /tuxjdk/dist ]] ; then
  if [[ -f /tuxjdk/dist/$OUTPUT.tar.xz ]] ; then
    rm -rf /tuxjdk/dist/$OUTPUT.tar.xz
  fi
else
  mkdir /tuxjdk/dist
fi
( cd building/images && mv j2sdk-image $OUTPUT && tar -cJf /tuxjdk/dist/$OUTPUT.tar.xz $OUTPUT )
# cleaning up:
chmod -R a+w /tuxjdk/build && rm -rf /tuxjdk/build
