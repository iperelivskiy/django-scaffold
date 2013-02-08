
import os
from fabric.api import local, settings, hide

quiet = lambda: settings(hide('everything'), warn_only=True)


def manage(command='help'):
    local('python src/{{ project_name }}/manage.py %s' % command)


def run():
    manage('runserver 0.0.0.0:8000')


def runplus():
    manage('runserver_plus 0.0.0.0:8000')


def shell():
    manage('shell_plus')


def syncdb(options='--migrate'):
    manage('syncdb %s' % options)


def migration(app, options='--auto'):
    manage('schemamigration %s %s' % (app, options))


def migrate(options=''):
    manage('migrate %s' % options)


def runtests(options=''):
    manage('test %s' % options)


def collectstatic():
    manage('collectstatic -v0 --noinput')
    manage('assets build')


def celery():
    with quiet():
        local('python src/{{ project_name }}/manage.py celerycam '
              '--pidfile=var/run/celeryev.pid &')
    _celery_worker()


def setup():
    if os.path.exists('tpl.gitignore'):
        local('mv tpl.gitignore .gitignore')
    if os.path.exists('tpl.README.md'):
        local('mv tpl.README.md README.md')
    local('rm -f LICENSE')
    local('mkdir -p var/log')
    local('mkdir -p var/run')
    local('mkdir -p var/media')
    local('mkdir -p var/static')
    local('pip install -r requirements/dev.txt')
    syncdb('--noinput --migrate')


def _celery_worker():
    local('reset')
    local('python src/{{ project_name }}/manage.py celery worker '
          '-E -B -l INFO &')
    with quiet():
        local('inotifywait -qe modify `find -name "*.py"`')
        local("ps auxww | grep 'celery worker' | awk '{print $2}' | "
              "xargs kill -9")
    _celery_worker()
