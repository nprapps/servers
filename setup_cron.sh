#!/bin/bash

# Server setup script for Ubuntu 14.04
# Must be executed with sudo!

set -x
exec 1> >(tee /var/log/server-setup.log) 2>&1

echo "Server setup beginning."

# Set locale
export LANG="en_US.UTF-8"

# Prompt for variables
echo "Enter your Amazon Access Key ID:"
read AWS_ACCESS_KEY_ID

echo "Enter your Amazon Secret Access Key:"
read AWS_SECRET_ACCESS_KEY

echo "Enter a hostname for this server:"
read HOSTNAME

echo "Enter a deployment target for this server:"
read DEPLOYMENT_TARGET

# Setup environment variables
echo "export DEPLOYMENT_TARGET=\"$DEPLOYMENT_TARGET\"" >> /etc/environment
echo "export AWS_ACCESS_KEY_ID=\"$AWS_ACCESS_KEY_ID\"" >> /etc/environment
echo "export AWS_SECRET_ACCESS_KEY=\"$AWS_SECRET_ACCESS_KEY\"" >> /etc/environment

# Ensure variables are available right now
source /etc/environment

# Setup default hostname
echo $HOSTNAME > /etc/hostname
echo "127.0.0.1 $HOSTNAME" > /etc/hosts
hostname $HOSTNAME

# Install outstanding updates
apt-get --yes update
apt-get --yes upgrade

# Install required packages
apt-get install --yes git openssh-server python2.7-dev libxml2-dev libxml2 libxslt1.1 libxslt1-dev build-essential python-pip mercurial subversion ruby rubygems libopenssl-ruby1.8 virtualenvwrapper nginx s3cmd npm
pip install uwsgi 
gem install scout

# Make sure SSH comes up on reboot
ln -s /etc/init.d/ssh /etc/rc2.d/S20ssh
ln -s /etc/init.d/ssh /etc/rc3.d/S20ssh
ln -s /etc/init.d/ssh /etc/rc4.d/S20ssh
ln -s /etc/init.d/ssh /etc/rc5.d/S20ssh

echo "Setup complete. Rebooting!"

reboot

