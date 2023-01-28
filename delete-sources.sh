#!/bin/bash

set -e
set -x

VERSION_BABEL=2_3_0
VERSION_PG=14_6

rm -f ./BABEL_${VERSION_BABEL}.tar.gz
touch ./BABEL_${VERSION_BABEL}.tar.gz
rm -f ./BABEL_${VERSION_BABEL}__PG_${VERSION_PG}.tar.gz
touch ./BABEL_${VERSION_BABEL}__PG_${VERSION_PG}.tar.gz
