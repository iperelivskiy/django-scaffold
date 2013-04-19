# {{ project_name|title }} #

## Install ##

- mkvirtualenv {{ project_name }}
- pip install fabric
- git clone git@github.com:company/{{ project_name }}.git
- cd {{ project_name }}
- fab setup run
