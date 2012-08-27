# Django 1.4 Project Template #

Django project template with Twitter bootstrap.

## Setup ##

Consider PROJECT_NAME as your real project name

- mkvirtualenv PROJECT_NAME
- $ pip install django
- $ pip install Fabric
- $ django-admin.py startproject --template=https://github.com/livskiy/django-project-template/zipball/master --extension="py,sh" --name="tpl.gitignore,tpl.README.md" PROJECT_NAME
- $ cd PROJECT_NAME
- $ fab setup
- $ fab runserver

Project settings live in src/PROJECT_NAME/PROJECT_NAME/conf dir. Dev settings are used by default.

## License ##

This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://opensource.org/licenses/BSD-3-Clause
