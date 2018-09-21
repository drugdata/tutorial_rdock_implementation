#!/bin/bash

# added cause local libstdc++.so.6 was being loaded instead of one shipped with openeye library
export RBT_ROOT="/opt/rDock_2013.1_src"
export LD_LIBRARY_PATH="/usr/lib/python2.7/site-packages/openeye/libs/python2.7-ucs4-linux-x64-g++4.x:$RBT_ROOT/lib:$LD_LIBRARY_PATH"
export PATH="$PATH:/opt/chimera/bin:$RBT_ROOT/bin"

exec /usr/bin/"$@"
