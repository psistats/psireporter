#!/bin/bash
###############################################################################
# Creates a debian source package then creates a deb file                     #
###############################################################################

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=$MY_DIR/..
ENV_DIR=$ROOT_DIR/.debenv
DIST_DIR=$ROOT_DIR/dist

cd $ROOT_DIR


VERSION="$( python setup.py --version )"
NAME="$( python setup.py --name )"



if [ -d "$DIST_DIR" ]; then
  rm -r $DIST_DIR
fi

if [ ! -d "$ENV_DIR" ]; then
  virtualenv -p python3 $ENV_DIR
fi

source $ENV_DIR/bin/activate

pip install stdeb

python setup.py sdist

cd $DIST_DIR

py2dsc $NAME-$VERSION.tar.gz

cd $DIST_DIR/deb_dist/$NAME-$VERSION

dpkg-buildpackage -rfakeroot -uc -us
