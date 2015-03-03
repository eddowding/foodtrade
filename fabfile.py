from fabric.api import env, run, sudo, local, prompt


def prod():
    env.name = 'prod'
    env.user = 'foodtrade'
    env.hosts = ['159.8.171.247']


def staging():
    env.name = 'staging'
    env.user = 'foodtrade'
    env.hosts = ['159.8.171.245']


def deploy():
    local('git fetch --tags')

    if env.name == 'staging':
        deploy_tag = None
    elif env.name == 'prod':
        local('git tag | sort -V | tail -5')
        deploy_tag = prompt('Choose tag to deploy: ')
        local('git tag | grep "%s"' % deploy_tag)

    if env.name == 'prod':
        checkout_cmd = 'git checkout tags/%s' % deploy_tag
    else:
        checkout_cmd = 'git checkout menu'
    sudo('cd /var/www; git fetch --tags')
    sudo('cd /var/www; %s' % checkout_cmd)
    sudo('cd /var/www; git pull origin %s' % deploy_tag)
    sudo('cd /var/www; pip install -r requirements.pip')
    sudo('cd /var/www; chown -R foodtrade:foodtrade bower_components')
    run('cd /var/www; ./manage.py bower install')
    sudo('cd /var/www; chown -R root:root bower_components')
    sudo('cd /var/www; ./manage.py collectstatic --noinput')
    sudo('chown www-data:www-data -R /var/www')
    sudo('service uwsgi restart')
    sudo('service nginx restart')

    if env.name == 'staging':
        create_tag = prompt('Does everything looks good, should we create tag? ', default='y')
        if create_tag.lower() == 'y':
            tag_name = prompt('Enter tag name [in format x.x.x]: ')
            local("git tag -a %s -m 'Fabric tagging %s'" % (tag_name, tag_name))
            local('git push --tags')
