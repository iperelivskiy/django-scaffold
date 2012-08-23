
import os
import sys
import site

# prevent errors with 'print' commands
sys.stdout = sys.stderr

# adopted from http://code.google.com/p/modwsgi/wiki/VirtualEnvironments
def add_to_path(dirs):
    # Remember original sys.path.
    prev_sys_path = list(sys.path)

    # Add each new site-packages directory.
    for directory in dirs:
        site.addsitedir(directory)

    # Reorder sys.path so new directories at the front.
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path

user = '{{ project_name }}'
site_packages_dir = '/home/%s/.virtualenvs/{{ project_name }}/lib/python2.7/site-packages' % user
project_dir = '/srv/www/{{ project_name }}'
project_src_dir = '%s/src/{{ project_name }}' % project_dir

add_to_path([
    os.path.normpath(site_packages_dir),
    os.path.normpath(project_dir),
    os.path.normpath(project_src_dir),
])

from {{ project_name }}.wsgi import application
