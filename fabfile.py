import contextlib

from fabric.api import *


env.hosts = ['fc',]
env.use_ssh_config = True

server_project_dir = '/opt/fc'
server_src_dir = '/'.join([server_project_dir, 'Farming-Concrete'])
server_virtualenv = 'fc'

server_front_dir = '/opt/mill'


@contextlib.contextmanager
def workon(ve):
    with prefix('workon %s' %ve):
        yield


@task
def pull():
    with cd(server_src_dir):
        run('git pull --no-edit')


@task
def test():
    local('DJANGO_SETTINGS_MODULE=barn.settings.test django-admin.py test farmingconcrete metrics')


@task
def build_static():
    with workon(server_virtualenv):
        run('django-admin.py collectstatic --noinput')

    with cd('/'.join([server_src_dir, 'barn/collected_static'])):
        run('bower install')

    with cd('/'.join([server_src_dir, 'barn/collected_static'])):
        run('r.js -o app.build.js')

    # Compress manually with uglifyjs
    with cd('/'.join([server_src_dir, 'barn/collected_static'])):
        run('uglifyjs main-built.js -m -c > main-built-compressed.js')

    # Replace main-built with compressed version
    with cd('/'.join([server_src_dir, 'barn/collected_static'])):
        run('mv main-built-compressed.js main-built.js')


@task
def install_requirements():
    with workon(server_virtualenv):
        with cd(server_src_dir):
            run('pip install -r requirements/base.txt')
            run('pip install -r requirements/production.txt')


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
    migrate()
    build_static()
    restart_django()


@task
def deploy_front():
    with cd(server_front_dir):
        run('git pull --no-edit')
