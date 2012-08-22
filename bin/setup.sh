#!/bin/bash

rm bin/setup.sh
rm `find -name '.removeme'`
mv tpl.gitignore .gitignore
mv tpl.README.md README.md
rm LICENSE
mkdir var/media
mkdir var/static
pip install -r requirements/dev.txt
