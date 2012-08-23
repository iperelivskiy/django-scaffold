#!/bin/bash

# Requirements
# inotify-tools. You can install it by typing: sudo apt-get install inotify-tools
# lessc. You can install it in your virtualenv by typing from project root: source bin/install_node.sh

echo "Listening for less files...";

while true;
    do inotifywait -qe modify `find -name "*.less"`;
    lessc "./static/less/main.less" "./static/css/main.css";
    if [ "$?" -eq "0" ]; then echo "Compiled."; fi
done;
