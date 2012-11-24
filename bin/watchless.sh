#!/bin/bash

# Requirements
# 1) inotify-tools. You can install it by typing: sudo apt-get install inotify-tools
# 2) lessc. You can install it in your virtualenv by typing from project root: source bin/install_node.sh

echo "Listening to less files...";

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR=${DIR%"/bin"}
LESS_DIR="$DIR/src/{{ project_name }}/{{ project_name}}/static/less"
CSS_DIR="$DIR/src/{{ project_name }}/{{ project_name}}/static/css"

while true;
    do inotifywait -qe modify `find -name "*.less"`;
    lessc "$LESS_DIR/main.less" "$CSS_DIR/main.css";
    if [ "$?" -eq "0" ]; then echo "Compiled."; fi
done;
