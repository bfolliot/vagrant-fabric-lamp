from fabric.api import *
from fabtools.vagrant import vagrant


@task
def upgrade():
     sudo('apt-get update')
     sudo('apt-get upgrade -y')

@task
def install():    
    print('Nothing to install')
