
import os

from fabric import network
from fabric.api import cd, run, env, prefix, abort, settings
from fabric.contrib import files


env.deploy_mode = 'prod'
env.user = '{{ project_name }}'
env.group = 'www'
env.sudo_user = 'root'
env.hosts = ['example.com']
env.project_name = '{{ project_name }}'
env.project_root = '/srv/www/%s' % env.project_name
env.project_src = '%s/src' % env.project_root
env.project_dir = '/'.join((env.project_src, env.project_name))
env.project_repo = 'git@bitbucket.org:company/{{ project_name }}.git'
env.var_dir = '%s/var' % env.project_root
env.env_dir = '/home/%s/.virtualenvs/%s' % (env.user, env.project_name)
env.python = '/usr/bin/python'
env.python_site_packages = '%s/lib/python2.7/site-packages' % env.env_dir
env.server_name = 'example.com'
env.server_admin = 'admin@example.com'


def manage(command='help'):
    with venv():
        with cd(env.project_root):
            run('python src/%s/manage.py %s' % (env.project_name, command))


def collectstatic():
    manage('collectstatic -v0 --noinput')


def syncdb(options='--migrate'):
    manage('syncdb %s' % options)


def migrate(options=''):
    manage('migrate %s' % options)


def shell():
    manage('shell_plus')


def pip(options='help'):
    with venv():
        with cd(env.project_root):
            run('pip %s' % options)


def pip_install(options=''):
    pip('install %s' % options)


def pip_install_requirements(options=''):
    pip_install('-r requirements/%s.txt %s' % (env.deploy_mode, options))


def pull():
    with cd(env.project_root):
        run('git pull origin master')


def hotfix():
    """
    Fast update the remote deployment codebase and restart.
    """
    pull()


def deploy():
    """
    Update the remote deployment, update the virtualenv, perform any
    pending migrations, then restart the wsgi process.
    """
    pull()
    pip_install_requirements()
    collectstatic()
    syncdb()


def nginx_restart():
    """
    Updates nginx config and restarts nginx.
    """
    _upload_template('%(deploy_mode)s/nginx.conf' % env,
                     '/etc/nginx/sites-available/%(project_name)s' % env)
    with settings(warn_only=True):
        sudo_run('ln -sf /etc/nginx/sites-available/%(project_name)s '
                 '/etc/nginx/sites-enabled/%(project_name)s' % env)
    sudo_run('service nginx reload')


def nginx_status():
    run('service nginx status')


def setup():
    """
    Setup the initial deploy environment.
    """
    run('mkdir -p %(project_root)s' % env)
    with cd(env.project_root):
        run('git clone %(project_repo)s .' % env)
        run('mkdir -p var/log')
        run('mkdir -p var/run')
        run('mkdir -p var/media')
        run('mkdir -p var/static')
    run('mkdir -p %(env_dir)s' % env)
    run('virtualenv -p %(python)s %(env_dir)s' % env)
    pip_install_requirements()
    syncdb('--noinput --migrate')


def version():
    """ Show last commit to the deployed repo. """
    with cd(env.project_root):
        run('git log -1')


def uname():
    """ Prints information about the host. """
    run("uname -a")


def sudo_run(*args, **kwargs):
    return _sudo_call(run, *args, **kwargs)


def venv():
    """
    Context manager. Use it for perform actions with virtualenv activated:

        with venv():
            # virtualenv is active here
            ...
    """
    return prefix('source %(env_dir)s/bin/activate' % env)


def _sudo_call(func, *args, **kwargs):
    old_user, host, port = network.normalize(env.host_string)
    env.host_string = network.join_host_strings(env.sudo_user, host, port)
    result = func(*args, **kwargs)
    env.host_string = network.join_host_strings(old_user, host, port)
    return result


def _upload_template(src, dst, **kwargs):
    if not os.path.isfile(src):
        abort('Template file %s not found.' % src)
    _sudo_call(files.upload_template, src, dst, env, **kwargs)
    run('less %s' % dst)
