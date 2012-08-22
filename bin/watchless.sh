#!/bin/bash

# Requires inotify-tools.
# You can install it by typing: sudo apt-get install inotify-tools

echo "Listening for less files...";

while true;
    do inotifywait -qe modify `find -name "*.less"`;
    lessc "./static/less/main.less" "./static/css/main.css";
    if [ "$?" -eq "0" ]; then echo "Compiled."; fi
done;
