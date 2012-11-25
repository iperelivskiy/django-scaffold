# Django Project Template #

Django project template with Twitter Bootstrap, H5BP and Fabric deployment scripts.

## Setup ##

- $ mkvirtualenv {project_name}
- $ pip install Django Fabric
- $ django-admin.py startproject --template=https://github.com/livskiy/djangoboot/zipball/master --extension="py,sh" --name="tpl.gitignore,tpl.README.md" {project_name}
- $ cd {project_name}
- $ fab setup run

Project settings live in src/{project_name}/{project_name}/conf dir. Dev settings are used by default.

## License ##

This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://opensource.org/licenses/BSD-3-Clause
