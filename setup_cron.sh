#!/bin/bash

# Server setup script for Ubuntu 14.04
# Must be executed with sudo!

set -x
exec 1> >(tee /var/log/server-setup.log) 2>&1

echo "Server setup beginning."

# Set locale
export LANG="en_US.UTF-8"

# Make sure SSH comes up on reboot
ln -s /etc/init.d/ssh /etc/rc2.d/S20ssh
ln -s /etc/init.d/ssh /etc/rc3.d/S20ssh
ln -s /etc/init.d/ssh /etc/rc4.d/S20ssh
ln -s /etc/init.d/ssh /etc/rc5.d/S20ssh

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
apt-get install --yes git openssh-server python2.7-dev libxml2-dev libxml2 libxslt1.1 libxslt1-dev build-essential python-pip mercurial subversion ruby virtualenvwrapper nginx s3cmd npm postgresql-client libpq-dev
pip install uwsgi 
gem install scout

# Configure scout
scout install GhUCqhYhVGUFHkCBw6U1BFJbmH46FU38Xkk7hXim

# Checkout configuration files
git clone https://github.com/nprapps/servers.git

# Install configuration files
cp servers/nginx/nginx.conf /etc/nginx/nginx.conf 
cp servers/nginx/sites-enabled/default /etc/nginx/sites-enabled/default 

mkdir /etc/nginx/locations-enabled
cp servers/nginx/locations-enabled/static /etc/nginx/locations-enabled/static
cp servers/nginx/locations-enabled/status /etc/nginx/locations-enabled/status

# Remove configuration files
rm -rf servers

# Create standard directories
mkdir /var/www
chown ubuntu:ubuntu /var/www

echo "Setup complete. Rebooting!"

reboot

