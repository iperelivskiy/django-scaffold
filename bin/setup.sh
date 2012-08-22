#!/bin/bash

SELF="$( cd "$( dirname "$0" )" && pwd )/bin/setup.sh"

if [ -f $SELF ]; then
	rm `find -name '.removeme'`
	mv tpl.gitignore .gitignore
	mv tpl.README.md README.md
	rm LICENSE
	mkdir -p var/media
	mkdir -p var/static
	pip install -r requirements/dev.txt
	rm bin/setup.sh
else
	echo "You should run setup from project root. Aborting."
fi
