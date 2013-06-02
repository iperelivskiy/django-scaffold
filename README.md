# Django Project Template #

A Django project template with Twitter Bootstrap, H5BP and Fabric deployment scripts.

## Setup ##

- $ mkvirtualenv {project_name}
- $ pip install django fabric
- $ django-admin.py startproject --template=https://github.com/livskiy/django-scaffold/archive/master.zip --extension="py,sh,tpl" {project_name}
- $ cd {project_name}
- $ fab setup run

Project settings live in src/{project_name}/baseapp/settings dir. Develop settings are used by default.
