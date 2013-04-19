# Django Project Template #

A Django project template with Twitter Bootstrap, H5BP and Fabric deployment scripts.

## Setup ##

- $ mkvirtualenv {project_name}
- $ pip install django fabric
- $ django-admin.py startproject --template=https://github.com/livskiy/django-boot/zipball/master --extension="py,sh" --name="tpl.gitignore,tpl.README.md" {project_name}
- $ cd {project_name}
- $ fab setup run

Project settings live in src/{project_name}/baseapp/settings dir. Dev settings are used by default.
