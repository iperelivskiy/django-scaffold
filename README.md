# Django 1.4 Project Template #

Django project template with Twitter bootstrap included.

## Installation ##

- сreate your virtualenv
- pip install django

Assume PROJECT_NAME as your real project name  

- $ django-admin.py startproject --template=/home/veter/Projects/sandbox/django_project_template --name="tpl.gitignore,tpl.README.md" PROJECT_NAME

Now you have PROJECT_NAME dir

- $ mv PROJECT_NAME/src/project PROJECT_NAME/src/PROJECT_NAME
- $ mv PROJECT_NAME/src/PROJECT_NAME/project_app PROJECT_NAME/src/PROJECT_NAME/PROJECT_NAME
- $ cd PROJECT_NAME
- $ source bin/install.sh
- edit src/PROJECT_NAME/PROJECT_NAME/conf/dev.py if needed
- $ python src/PROJECT_NAME/manage.py runserver

## License ##

This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://opensource.org/licenses/BSD-3-Clause
