
import os
from fabric.api import local


def manage(command):
    local("python src/{{ project_name }}/manage.py %s" % command)


def run():
    manage('runserver_plus 0.0.0.0:8000')


def shell():
    manage('shell_plus')


def syncdb(options=''):
    manage('syncdb %s' % options)


def migration(app, options='--auto'):
    manage('schemamigration %s %s' % (app, options))


def migrate(options=''):
    manage('migrate %s' % options)


def runtests(options=''):
    manage('test %s' % options)


def setup():
    local('rm -f `find -name ".removeme"`')
    if os.path.exists('tpl.gitignore'):
        local('mv tpl.gitignore .gitignore')
    if os.path.exists('tpl.README.md'):
        local('mv tpl.README.md README.md')
    local('rm -f LICENSE')
    local('mkdir -p var/media')
    local('mkdir -p var/static')
    local('pip install -r requirements/dev.txt')
    local('echo "from {{ project_name }}.conf.dev import *" > src/{{ project_name }}/{{ project_name }}/settings.py')
    syncdb()
