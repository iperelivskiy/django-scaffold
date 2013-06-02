
import os

from fabric import network
from fabric.api import cd, run, env, prefix


env.deploy_mode = 'production'
env.hosts = ['{{ project_name }}.com']

env.server_name = '{{ project_name }}.com'
env.server_admin = 'admin@{{ project_name }}.com'
env.user = '{{ project_name }}'
env.sudo_user = 'root'
env.project_name = '{{ project_name }}'
env.project_root = '/home/%(user)s/www/%(project_name)s' % env
env.project_src = '%(project_root)s/src' % env
env.project_repo = 'git@github.com:company/{{ project_name }}.git'
env.var_dir = '%(project_root)s/var' % env
env.virtualenv_dir = '/home/%(user)s/.virtualenvs/%(project_name)s' % env
env.python = '%(virtualenv_dir)s/bin/python' % env
env.managepy = '%(project_root)s/deploy/%(deploy_mode)s/manage.py' % env


def manage(command='help'):
    with virtualenv():
        run('python %s %s' % (env.managepy, command))


def syncdb(options='--migrate'):
    manage('syncdb %s' % options)


def migrate(options=''):
    manage('migrate %s' % options)


def buildstatic():
    manage('collectstatic -v0 --noinput')


def pip(options='help'):
    with virtualenv():
        with cd(env.project_root):
            run('pip %s' % options)


def pip_install(options=''):
    pip('install %s' % options)


def pip_install_requirements(options=''):
    pip_install('-r requirements/%s.txt %s' % (env.deploy_mode, options))


def pull():
    with cd(env.project_root):
        run('git pull origin master')


def supervisor(command='status'):
    sudo('supervisorctl %s' % command)


def restart_app():
    supervisor('restart {{ project_name }}-app')


def restart_services():
    # supervisor('restart {{ project_name }}-celerybeat')
    # supervisor('restart {{ project_name }}-celerycam')
    # supervisor('restart {{ project_name }}-celeryd')
    # supervisor('restart {{ project_name }}-thumbor')
    restart_app()


def nginx(command='status'):
    sudo('service nginx %s' % command)


def hotfix():
    """
    Fast update the remote deployment codebase and restart an app server.
    """
    pull()
    clear_pyc()
    restart_app()


def deploy():
    """
    Update the remote deployment, update the virtualenv, perform any
    pending migrations, then restart services.
    """
    pull()
    clear_pyc()
    pip_install_requirements()
    buildstatic()
    syncdb()
    restart_services()


def clear_pyc():
    with cd(env.project_root):
        run('find -name "*.pyc" -delete')


def setup():
    """
    Setup the initial deploy environment.
    """
    run('mkdir -p %(project_root)s' % env)
    with cd(env.project_root):
        run('git clone %(project_repo)s .' % env)
        run('mkdir -p var/log')
        run('mkdir -p var/media')
        run('mkdir -p var/run')
        run('mkdir -p var/static')

    run('mkdir -p %(virtualenv_dir)s' % env)
    run('virtualenv %(virtualenv_dir)s --no-site-packages' % env)

    sudo('ln -sf %(project_root)s/deploy/%(deploy_mode)s/conf/'
         'supervisor.app.conf '
         '/etc/supervisor/conf.d/%(project_name)s.app.conf' % env)
    supervisor('reload')

    sudo('ln -sf %(project_root)s/deploy/%(deploy_mode)s/conf/nginx.conf '
         '/etc/nginx/sites-enabled/%(project_name)s.conf' % env)
    nginx('restart')

    deploy()


def configure():
    """
    Make config files from templates.
    """
    base_dir = os.path.join(os.path.dirname(__file__), env.deploy_mode)
    conf_templates_dir = os.path.join(base_dir, 'conf_templates')
    os.system('mkdir -p %s' % os.path.join(base_dir, 'conf'))

    for path, dirs, files in os.walk(conf_templates_dir):
        conf_dir = path.replace('conf_templates', 'conf', 1)
        for filename in files:
            conf_template_path = os.path.join(path, filename)
            conf_path = os.path.join(conf_dir, filename)
            conf_template = open(conf_template_path).read()
            with open(conf_path, 'w') as conf:
                conf.write(conf_template % env)
                print conf_path


def version():
    """ Show last commit to the deployed repo. """
    with cd(env.project_root):
        run('git log -1')


def uname():
    """
    Prints information about the host.
    """
    run("uname -a")


def virtualenv():
    """
    Context manager. Use it for perform actions with virtualenv activated:

        with virtualenv():
            # Inside virtualenv.
            ...
    """
    return prefix('source %(virtualenv_dir)s/bin/activate' % env)


def sudo(*args, **kwargs):
    return _sudo(run, *args, **kwargs)


def _sudo(func, *args, **kwargs):
    old_user, host, port = network.normalize(env.host_string)
    env.host_string = network.join_host_strings(env.sudo_user, host, port)
    result = func(*args, **kwargs)
    env.host_string = network.join_host_strings(old_user, host, port)
    return result


# def _upload_template(src, dst, **kwargs):
#     if not os.path.isfile(src):
#         abort('Template file %s not found.' % src)
#     _sudo(files.upload_template, src, dst, env, **kwargs)
#     run('less %s' % dst)
# def nginx_restart():
#     """
#     Updates nginx config and restarts nginx.
#     """
#     _upload_template('%(deploy_mode)s/nginx.conf' % env,
#                      '/etc/nginx/sites-available/%(project_name)s' % env)
#     with settings(warn_only=True):
#         sudo('ln -sf /etc/nginx/sites-available/%(project_name)s '
#                  '/etc/nginx/sites-enabled/%(project_name)s' % env)

# def nginx_status():
#     run('service nginx status')
