#!/usr/bin/env python

from fabric.api import *
from fabric.contrib.files import *
from fabric.contrib.project import rsync_project

"""
Base configuration
"""
env.user = 'ubuntu'
env.python = 'python2.7'
env.forward_agent = True
env.project_name = 'servers'
env.repo_path = '/home/ubuntu/%(project_name)s' % env
env.nginx_path = '/etc/nginx'
env.site_paths = ['sites-available', 'sites-enabled']


@task
def production():
    env.settings = 'production'
    env.hosts = ['54.245.114.14', '50.112.9.120']


@task
def staging():
    env.settings = 'staging'
    env.hosts = ['50.112.92.131', '50.112.87.147']


@task
def write_nginx_confs():
    require('settings', provided_by=[production, staging])

    sudo('chmod -R 777 /etc/nginx')

    for path in ['sites-enabled/default', 'sites-available/']:
        if exists('%s/%s' % (env.nginx_path, path), use_sudo=True):
            run('rm -rf %s/%s' % (env.nginx_path, path))

    rsync_project(env.nginx_path, 'nginx/', extra_opts='-O')

    sudo('chown -R root:root /etc/nginx')
    sudo('chmod -R 755 /etc/nginx')


def reload_nginx():
    require('settings', provided_by=[production, staging])
    sudo('service nginx reload')


@task
def deploy(remote='origin'):
    require('settings', provided_by=[production, staging])

    write_nginx_confs()
    reload_nginx()
