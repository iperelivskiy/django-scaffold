#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR=${DIR%"/bin"}
cd $DIR

rm `find -name '.removeme'`
mv tpl.gitignore .gitignore
mv tpl.README.md README.md
rm LICENSE
mkdir -p var/media
mkdir -p var/static
pip install -r requirements/dev.txt
rm bin/setup.sh
