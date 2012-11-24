
import re
import os

from fabric import network
from fabric.api import (cd, run, env, prefix, abort, settings, hide,
                        puts, warn)
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

# Apache
env.apache_processes = 1
env.apache_threads = 15
env.apache_ports_file = '/etc/apache2/ports-fabric.conf'
env.apache_ports_range = (50001, 60000)


def manage(command='help'):
    with venv():
        with cd(env.project_root):
            run('python src/%s/manage.py %s' % (env.project_name, command))


def collectstatic():
    manage('collectstatic -v0 --noinput')
    manage('assets build')


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


def touch_wsgi():
    run('touch %(project_root)s/deploy/%(deploy_mode)s/wsgi.py' % env)


def hotfix():
    """
    Fast update the remote deployment codebase and restart the wsgi process.
    """
    pull()
    touch_wsgi()


def deploy():
    """
    Update the remote deployment, update the virtualenv, perform any
    pending migrations, then restart the wsgi process.
    """
    pull()
    pip_install_requirements()
    collectstatic()
    syncdb()
    touch_wsgi()


def nginx_restart():
    """
    Updates nginx config and restarts nginx.
    """
    _setup_apache_port()
    _upload_template('%(deploy_mode)s/nginx.conf' % env,
                     '/etc/nginx/sites-available/%(project_name)s' % env)
    with settings(warn_only=True):
        sudo_run('ln -sf /etc/nginx/sites-available/%(project_name)s '
                 '/etc/nginx/sites-enabled/%(project_name)s' % env)
    sudo_run('service nginx reload')


def nginx_status():
    run('service nginx status')


def apache_restart():
    """
    Updates apache config and restarts apache.
    """
    _setup_apache_port()
    _upload_template('%(deploy_mode)s/apache.conf' % env,
                     '/etc/apache2/sites-available/%s' % env.project_name)
    sudo_run('a2ensite %(project_name)s' % env)
    sudo_run('service apache2 reload')


def apache_status():
    run('service apache2 status')


def apache_access_log():
    run('tail -f %(var_dir)s/log/apache.access.log' % env)


def apache_error_log():
    run('tail -f %(var_dir)s/log/apache.error.log' % env)


def setup():
    """
    Setup the initial deploy environment.
    """
    #run('rm -rf %(project_root)s' % env)  # Be careful with env.project_root!
    run('mkdir -p %(project_root)s' % env)
    with cd(env.project_root):
        run('git clone %(project_repo)s .' % env)
        run('mkdir -p var/media')
        run('mkdir -p var/static')
        run('mkdir -p var/log')
        run('echo "from %(project_name)s.conf.%(deploy_mode)s import *" > '
            'src/%(project_name)s/%(project_name)s/settings.py' % env)
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


def _setup_apache_port():
    """
    Makes sure some port is correctly listened in :file:`ports.conf` and
    sets :attr:`env.apache_port` to this port.
    """
    TAKEOVER_STRING = '# This file is managed by fab scripts.'
    lines = _ports_lines()

    # Take over ports.conf
    if not lines or lines[0] != TAKEOVER_STRING:
        lines = [TAKEOVER_STRING]

    used_ports = _used_ports(lines)

    for port in used_ports:
        if used_ports[port] == env.project_name:
            # instance is binded to port
            env.apache_port = port
            print '*** Instance is binded to port %s ***' % port
            return

    # Instance is not binded to any port yet.
    # Find an empty port and listen to it.
    for port in range(*env.apache_ports_range):
        if str(port) not in used_ports:
            # Port is found.
            lines.extend([
                '',
                '# Used by ' + env.project_name,
                'Listen 127.0.0.1:' + str(port)
            ])
            env.apache_port = port
            puts('Instance is not binded to any port. '
                 'Binding it to port ' + str(port))
            sudo_run("echo '%s\n' > %s" % ('\n'.join(lines),
                     env.apache_ports_file))
            return

    warn('All apache ports are used!')


def _ports_lines():
    with settings(hide('stdout')):
        ports_data = sudo_run('cat ' + env.apache_ports_file)
    return ports_data.splitlines()


def _used_ports(lines):
    ports_mapping = dict()
    listen_re = re.compile('^Listen (?P<host>.+):\s*(?P<port>\d+)')
    instance_re = re.compile('^# Used by (?P<instance>.+)')

    for index, line in enumerate(lines):
        match = re.match(listen_re, line)
        if match:
            instance = None
            if index:
                instance_match = re.match(instance_re, lines[index - 1])
                if instance_match:
                    instance = instance_match.group('instance')
            ports_mapping[match.group('port')] = instance
    return ports_mapping
