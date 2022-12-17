#!/bin/bash

set -e
set -x

VERSION_BABEL=2_2_0
VERSION_PG=14_5

rm ./BABEL_${VERSION_BABEL}.tar.gz
touch ./BABEL_${VERSION_BABEL}.tar.gz
rm ./BABEL_${VERSION_BABEL}__PG_${VERSION_PG}.tar.gz
touch ./BABEL_${VERSION_BABEL}__PG_${VERSION_PG}.tar.gz
