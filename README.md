NPR Apps Servers
================

These scripts are designed to turn a brand new Ubuntu 12.04 server image into a fully functional server.

It is expected that AMI snapshots will be taken of each server and used for routine spin-ups, but these scripts allow us to quickly modify the basic recipe. (And track changes.)

Remember: **never make a baked AMI public.**

## Creating servers

If creating servers with the web console isn't fast enough for you, then you can create servers from the command line with the EC2 API tools. Install them with:

``brew install ec2-api-tools``

At the end of the installation a set of environment variables to be set will be printed. Be sure to add these to your ``~/.bash_profile``. You will also need to download a private key and X.509 certificate from AWS. Update the ``EC2_PRIVATE_KEY`` and ``EC2_CERT`` environment variables to point to these files.

Once configured you can create a new server from your command line:

* Create server: ``ec2-run-instances ami-1cdd532c -t t1.micro --region us-west-2 --key nprapps``
* Get server DNS name: ``ec2-describe-instances --region us-west-2 $INSTANCE_ID`` (keep running until available)

## Cron

Creating a new cron/basic server:

* SSH in: ``ssh -i ~/.ssh/nprapps.pem ubuntu@$SERVER_DNS_NAME``
* Fetch setup script: ``wget https://raw.github.com/nprapps/servers/master/setup_cron.sh``
* Run setup script: ``sudo bash setup_cron.sh``
* Type in configuration values and wait for script to complete.
* ``rm setup_cron.sh``

## Database

TODO

## Application

TODO

