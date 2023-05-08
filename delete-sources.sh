#!/bin/bash

set -e
set -x

VERSION_BABEL=3_1
VERSION_PG=15_2

rm -f ./BABEL_${VERSION_BABEL}.tar.gz
touch ./BABEL_${VERSION_BABEL}.tar.gz
rm -f ./BABEL_${VERSION_BABEL}__PG_${VERSION_PG}.tar.gz
touch ./BABEL_${VERSION_BABEL}__PG_${VERSION_PG}.tar.gz
