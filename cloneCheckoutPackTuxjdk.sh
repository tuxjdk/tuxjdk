#!/bin/bash

readonly TAG="$1"
readonly GIT="$( which git 2>/dev/null )"
readonly TAR="$( which tar 2>/dev/null )"

if [[ -n "$2" ]] ; then
  readonly UPSTREAM="$2"
else
  readonly UPSTREAM='https://github.com/TheIndifferent/tuxjdk.git'
fi

if [[ -z $TAG ]] ; then
  readonly NAME='tuxjdk'
else
  readonly NAME="tuxjdk-$TAG"
fi

if [[ -z $GIT ]] ; then
  echo 'git was not found' >&2
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

echo -e "\e[0;35mCloning the source from '$UPSTREAM'...\e[0m"
( $GIT clone "$UPSTREAM" "$NAME" )

if [[ -n $TAG ]] ; then
  echo -e '\e[0;35mChecking out the tag...\e[0m'
  ( cd "$NAME" && $GIT checkout "$TAG" )
fi

echo -e '\e[0;35mCreating tarball...\e[0m'
( tar --exclude-vcs -cJf "$NAME.tar.xz" "$NAME" )

echo -e '\e[0;35mDone.\e[0m'
