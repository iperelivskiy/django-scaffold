# {{ project_name|title }} #

## Install ##

- mkvirtualenv {{ project_name }}
- pip install Fabric
- git clone git@bitbucket.org:amigaz/{{ project_name }}.git
- cd {{ project_name }}
- fab setup
- fab runserver
