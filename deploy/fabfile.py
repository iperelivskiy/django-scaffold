import os
import string

from fabric.api import cd, run, env, local, sudo, require
from fabric.operations import _prefix_commands, _prefix_env_vars


env.user = '{{ project_name }}'
env.hosts = ['{{ project_name }}.com']
env.project_dir = '/srv/www/{{ project_name }}'
env.project_repo = 'git@bitbucket.org:amigaz/{{ project_name }}.git'
env.env_dir = '/home/%s/.virtualenvs/{{ project_name }}' % env.user
env.django_settings_module = '{{ project_name }}.settings'


def deploy_static():
    with cd(env.project_dir):
        run('python manage.py collectstatic -v0 --noinput')


def uname():
    """ Prints information about the host. """
    run("uname -a")


def push():
    """ Push new code and pull on all hosts """
    local('git push origin master')
    with cd(env.project_dir):
        run('git pull origin master')


def update_requirements():
    """ Update requirements in the virtualenv. """
    run("%s/bin/pip install -r %s/requirements/prod.txt" % (env.env_dir, env.project_dir))


def migrate(app=None):
    """
    Run the migrate task
    Usage: fab migrate:app_name
    """
    if app:
        run("source %s/bin/activate; django-admin.py migrate %s --settings=%s" % (env.env_dir, app, env.django_settings_module))
    else:
        run("source %s/bin/activate; django-admin.py migrate --settings=%s" % (env.env_dir, env.django_settings_module))


def version():
    """ Show last commit to the deployed repo. """
    with cd(env.project_dir):
        run('git log -1')


def restart():
    """ Restart the wsgi process """
    run("touch %s/deploy/prod/wsgi.py" % env.project_dir)


def ve_run(cmd):
    """
    Helper function.
    Runs a command using the virtualenv environment
    """
    require('root')
    return sshagent_run('source %s/bin/activate; %s' % (env.env_dir, cmd))


def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent.
    This helper uses your system's ssh to do so.
    """
    # Handle context manager modifications
    wrapped_cmd = _prefix_commands(_prefix_env_vars(cmd), 'remote')
    try:
        host, port = env.host_string.split(':')
        return local(
            "ssh -p %s -A %s@%s '%s'" % (port, env.user, host, wrapped_cmd)
        )
    except ValueError:
        return local(
            "ssh -A %s@%s '%s'" % (env.user, env.host_string, wrapped_cmd)
        )


def deploy():
    """ Update the remote deployment, update the virtualenv, perform any
    pending migrations, then restart the wsgi process """
    push()
    update_requirements()
    migrate()
    restart()


def bootstrap():
    """ Bootstrap the initial deploy environment """
    run('mkdir -p %s' % (env.project_dir))
    run('virtualenv %s' % (env.env_dir))
    with cd(env.project_dir):
        run('git clone %s .' % (env.project_repo))
        run('mkdir -p var/media')
        run('mkdir -p var/static')
        run('echo "from {{ project_name }}.conf.prod import *" > src/{{ project_name }}/{{ project_name }}/settings.py')
