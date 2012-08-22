# Django 1.4 Project Template #

Django project template with Twitter bootstrap included.

## Setup ##

Consider PROJECT_NAME as your real project name

- сreate your virtualenv
- $ pip install django
- $ django-admin.py startproject --template=https://github.com/livskiy/django-project-template/zipball/master --name="tpl.gitignore,tpl.README.md" PROJECT_NAME
- $ cd PROJECT_NAME
- $ source bin/setup.sh
- $ python src/PROJECT_NAME/manage.py runserver

Project settings live in src/PROJECT_NAME/PROJECT_NAME/conf dir. Dev settings are used by default.

## License ##

This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://opensource.org/licenses/BSD-3-Clause
