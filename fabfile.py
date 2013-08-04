from fabric.api import *


env.hosts = ['wf',]
env.use_ssh_config = True

server_project_dir = '~/webapps/fc_barn_dev'
server_src_dir = '/'.join([server_project_dir, 'Farming-Concrete'])
server_virtualenv = 'Farming-Concrete'


@task
def pull():
    with cd(server_src_dir):
        run('git pull')


@task
def build_static():
    with prefix('workon ' + server_virtualenv):
        run('django-admin.py collectstatic --noinput')

    # TODO reenable if we are using r.js
    #with cd('/'.join([server_src_dir, 'barn/collected_static/js/']):
        #run('r.js -o app.build.js')


@task
def install_requirements():
    with prefix('workon ' + server_virtualenv):
        run('pip install -r Farming-Concrete/requirements/base.txt')
        run('pip install -r Farming-Concrete/requirements/production.txt')


@task
def syncdb():
    with prefix('workon ' + server_virtualenv):
        run('django-admin.py syncdb')


@task
def migrate():
    with prefix('workon ' + server_virtualenv):
        run('django-admin.py migrate')


@task
def restart_django():
    with prefix('workon ' + server_virtualenv):
        run('supervisorctl -c ~/supervisor/supervisord.conf restart django')


@task
def restart_memcached():
    run('supervisorctl -c ~/supervisor/supervisord.conf restart memcached')


@task
def status():
    with prefix('workon ' + server_virtualenv):
        run('supervisorctl -c ~/supervisor/supervisord.conf status')


@task
def dev_test():
    pull()
    install_requirements()
    syncdb()
    migrate()
    build_static()
    dev_supervisor()


@task
def dev_supervisor():
    with prefix('workon ' + server_virtualenv):
        run('supervisord -c ~/supervisor/supervisord.conf')


@task
def dev_supervisor_shutdown():
    with prefix('workon ' + server_virtualenv):
        run('supervisorctl -c ~/supervisor/supervisord.conf shutdown')


@task
def deploy():
    pull()
    install_requirements()
    syncdb()
    migrate()
    build_static()
    restart_django()
