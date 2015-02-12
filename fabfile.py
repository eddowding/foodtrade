from fabric.api import env, run, sudo

def prod():
    env.user = 'foodtrade'
    env.hosts = ['ftmenuvm.cloudapp.net']

def staging():
    env.user = 'foodtrade'
    env.hosts = ['159.8.171.245']

def deploy():
    sudo('cd /var/www; git pull')
    sudo('cd /var/www; pip install -r requirements.pip')
    sudo('cd /var/www; chown -R foodtrade:foodtrade bower_components')
    run('cd /var/www; ./manage.py bower install')
    sudo('cd /var/www; chown -R root:root bower_components')
    sudo('cd /var/www; ./manage.py collectstatic --noinput')
    sudo('chown www-data:www-data -R /var/www')
    sudo('service uwsgi restart')
    sudo('service nginx restart')
