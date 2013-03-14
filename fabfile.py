#!/usr/bin/env python

from fabric.api import *

"""
Base configuration
"""
env.user = 'ubuntu'
env.python = 'python2.7'
env.forward_agent = True
env.project_name = 'servers'
env.repo_path = '/home/ubuntu/%(project_name)s/' % env

PRODUCTION_SERVERS = ['54.245.114.14']
STAGING_SERVERS = ['50.112.92.131']


@task(alias='prod')
def production():
    env.settings = 'production'
    env.hosts = PRODUCTION_SERVERS


@task(alias='stg')
def staging():
    env.settings = 'staging'
    env.hosts = STAGING_SERVERS


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


def update_nginx():
    run('uname -r')


@task
def deploy(remote='origin'):
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])

    confirm_branch()
    checkout_latest(remote)
    update_nginx()
