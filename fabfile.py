from fabric.api import env, run
from fabric.contrib.files import *
from fabric.decorators import runs_once
from fabric.operations import *
from datetime import *

DOMAIN = '.cloudapp.net'
CHEF_VERSION = '12.10.24'
CHEF_BINARY = '/usr/bin/chef-client'

HOSTS = {
    'test': ['fa-stage']
}

env.user = 'tpalko'

@runs_once
def setup_hosts(environment):
    env.hosts = [ "%s%s" %(h, DOMAIN) for h in HOSTS[environment] ]

@runs_once
def package():
    local('tar --exclude \*.pyc --exclude deploy.tar.gz --exclude .vagrant --exclude .git -czf deploy.tar.gz .')

def deploy(environment):

    sudo('rm -rf /var/chef') 
    sudo('mkdir -p /var/chef') 
    put('deploy.tar.gz', '/var/chef', use_sudo=True)

    with cd('/var/chef'):
        sudo('tar -xzf deploy.tar.gz')

    if not exists(CHEF_BINARY, use_sudo=True):
        sudo('curl -L https://www.opscode.com/chef/install.sh | sudo bash -s --')

    with cd('/var/chef'):
        sudo('%s --local-mode -c client.rb -E %s' %(CHEF_BINARY, environment))

@runs_once
def clean():
    local('rm deploy.tar.gz')