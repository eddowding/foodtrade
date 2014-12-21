from fabric.api import env, run, sudo

def staging():
    env.user = 'foodtrade'
    env.hosts = ['ftmenuvm.cloudapp.net']

def deploy():
    sudo('cd /var/www; git pull')
    sudo('cd /var/www; chown -R foodtrade:foodtrade bower_components')
    run('cd /var/www; ./manage.py bower install')
    sudo('cd /var/www; chown -R root:root bower_components')
    sudo('cd /var/www; ./manage.py collectstatic -l --noinput')
    sudo('service uwsgi restart')
    sudo('service nginx restart')
