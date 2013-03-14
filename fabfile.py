#!/usr/bin/env python

import os

from fabric.api import *
from fabric.contrib.files import *

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
    env.hosts = ['54.245.114.14']


@task(alias='stg')
def staging():
    env.settings = 'staging'
    env.hosts = ['50.112.92.131']


@task
def stable():
    """
    Work on stable branch.
    """
    env.branch = 'stable'


@task
def master():
    """
    Work on development branch.
    """
    env.branch = 'master'


@task
def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name


def confirm_branch():
    """
    Confirm a production deployment.
    """
    if (env.settings == 'production' and env.branch != 'stable'):
        answer = prompt("You are trying to deploy the '%(branch)s' branch to production.\nYou should really only deploy a stable branch.\nDo you know what you're doing?" % env, default="Not at all")
        if answer not in ('y', 'Y', 'yes', 'Yes', 'buzz off', 'screw you'):
            exit()


def checkout_latest(remote='origin'):
    """
    Checkout the latest source.
    """
    require('settings', provided_by=[production, staging])

    env.remote = remote

    run('cd %(repo_path)s; git fetch %(remote)s' % env)
    run('cd %(repo_path)s; git checkout %(branch)s; git pull %(remote)s %(branch)s' % env)


def link_nginx_sites():
    require('settings', provided_by=[production, staging])

    for path, dirs, files in os.walk('nginx/sites-available'):
        for site in files:
            for remote_path in env.site_paths:
                if not exists('%s/%s/%s' % (env.nginx_path, remote_path, site), use_sudo=True):
                    sudo('ln -s %s/nginx/sites-available/%s %s/%s/%s' % (
                        env.repo_path, site,
                        env.nginx_path, remote_path, site))


def reload_nginx():
    require('settings', provided_by=[production, staging])
    sudo('service nginx reload')


@task
def deploy(remote='origin'):
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])

    confirm_branch()
    checkout_latest(remote)
    link_nginx_sites()
    reload_nginx()


@task
def shiva_the_destroyer():
    require('settings', provided_by=[production, staging])

    for remote_path in env.site_paths:
        sudo('rm -rf %s/%s/*' % (env.nginx_path, remote_path))
