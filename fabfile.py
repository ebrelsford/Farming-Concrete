import contextlib

from fabric.api import *


env.hosts = ['fc',]
env.use_ssh_config = True

server_project_dir = '/opt/fc'
server_src_dir = '/'.join([server_project_dir, 'Farming-Concrete'])
server_virtualenv = 'fc'


@contextlib.contextmanager
def workon(ve):
    with prefix('workon %s' %ve):
        yield


@task
def pull():
    with cd(server_src_dir):
        run('git pull')


@task
def build_static():
    with workon(server_virtualenv):
        run('django-admin.py collectstatic --noinput')

    with cd('/'.join([server_src_dir, 'barn/collected_static'])):
        run('bower install')

    with cd('/'.join([server_src_dir, 'barn/collected_static'])):
        run('r.js -o app.build.js')


@task
def install_requirements():
    with workon(server_virtualenv):
        with cd(server_src_dir):
            run('pip install -r requirements/base.txt')
            run('pip install -r requirements/production.txt')


@task
def syncdb():
    with workon(server_virtualenv):
        run('django-admin.py syncdb')


@task
def migrate():
    with workon(server_virtualenv):
        run('django-admin.py migrate')


@task
def restart_django():
    sudo('supervisorctl restart fc_django')


@task
def restart_memcached():
    sudo('supervisorctl restart memcached')


@task
def status():
    sudo('supervisorctl status')


@task
def deploy():
    pull()
    install_requirements()
    syncdb()
    migrate()
    build_static()
    restart_django()
