#!/bin/sh
export JAVA_HOME='/opt/tuxjdk'
/opt/tuxjdk/bin/$( basename "${BASH_SOURCE[0]}" ) "$@"
