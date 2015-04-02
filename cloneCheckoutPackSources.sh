#!/bin/bash

readonly TAG="$1"
readonly HG="$( which hg 2>/dev/null )"
readonly TAR="$( which tar 2>/dev/null )"

readonly UPSTREAM='http://hg.openjdk.java.net/jdk8u/jdk8u'

if [[ -z $TAG ]] ; then
  readonly NAME='jdk8u'
else
  readonly NAME="$TAG"
fi

if [[ -z $HG ]] ; then
  echo 'hg was not found' >&2
  exit 1
fi
if [[ -z $TAR ]] ; then
  echo 'tar was not found' >&2
  exit 1
fi

if [[ -a "$NAME" ]] ; then
  echo "'$NAME' file or folder already exists" >&2
  exit 1
fi
if [[ -a "$NAME.tar.xz" ]] ; then
  echo "'$NAME.tar.xz' file or folder already exists" >&2
  exit 1
fi

echo -e '\e[0;35mCloning the source...\e[0m'
( $HG clone "$UPSTREAM" "$NAME" && cd "$NAME" && bash 'get_source.sh' )

if [[ -n $TAG ]] ; then
  echo -e '\e[0;35mChecking out the tag...\e[0m'
  ( cd "$NAME" && bash ./common/bin/hgforest.sh checkout "$TAG" )
fi

echo -e '\e[0;35mCreating tarball...\e[0m'
( tar --exclude-vcs --exclude-vcs-ignores -cJf "$NAME.tar.xz" "$NAME" )

echo -e '\e[0;35mDone.\e[0m'
