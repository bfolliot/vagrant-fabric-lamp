from fabric.api import *
from fabtools.vagrant import vagrant
from fabtools.require.deb import packages
from fabtools.require.mysql import server as mysql
from fabtools.require.apache import server as apache, site_disabled, site_enabled, site
from fabtools.require.service import stopped, restarted
from fabtools.require.files import template_file, directory
from os.path import dirname, realpath

@task
def upgrade():
     sudo('apt-get update')
     sudo('apt-get upgrade -y')

@task
def install():
    packages([
        'build-essential',
        'php5',
        'php5-mysql',
    ], update=False)

    mysql(password="vagrant")

    apache()
    stopped('apache2')
    full_path = dirname(realpath(__file__))
    # template_file(
    #     template_source = full_path + '/templates/apache2/vhost.tpl',
    #     path='/etc/apache2/sites-available/mylampvm.dev',
    #     context = {
    #         'server_name': 'mylampvm.dev',
    #         'document_root': '/srv/htdocs',
    #         'port' : 80
    #     },
    #     owner = 'root',
    #     group = 'root',
    #     use_sudo=True
    # )
    site_disabled('default')
    site(
        'mylampvm.dev',
        template_source=full_path + '/templates/apache2/vhost.tpl',
        port=80,
        server_name='mylampvm.dev',
        document_root='/srv/htdocs',
    )

    template_file(
        template_source = full_path + '/templates/apache2/envvars.tpl',
        path='/etc/apache2/envvars',
        context = {
            'apache_run_user': 'vagrant',
            'apache_run_group': 'vagrant',
        },
        owner = 'root',
        group = 'root',
        use_sudo=True
    )
    directory('/var/lock/apache2', True, 'vagrant', 'vagrant')
    
    # site_enabled('mylampvm.dev')
    restarted('apache2')
