NPR Visuals Servers
===================

* [About servers](#about-servers)
* [Creating EC2 servers](#creating-ec2-servers)
* [Configuring a server](#configuring-a-server)

About Servers
--------------

**Note:** If you're looking for a list of our servers, see our [Server Census](https://docs.google.com/spreadsheet/ccc?key=0AjWpFWKpoFHqdFl2cGxaVklCR1dPUnBGZkFTTVZQZUE&usp=drive_web#gid=0).

These scripts are designed to turn a brand new Ubuntu server image into a fully functional server.

It is expected that AMI snapshots will be taken of each server and used for routine spin-ups, but these scripts allow us to quickly modify the basic recipe. (And track changes.)

Remember: **never make a baked AMI public.**

Creating EC2 servers
--------------------

If creating servers with the web console isn't fast enough for you, then you can create servers from the command line with the EC2 API tools. Install them with:

``brew install ec2-api-tools``

At the end of the installation a set of environment variables to be set will be printed. Be sure to add these to your ``~/.bash_profile``. You will also need to download a private key and X.509 certificate from AWS. Update the ``EC2_PRIVATE_KEY`` and ``EC2_CERT`` environment variables to point to these files.

Once configured you can create a new server from your command line:

* Create server: ``ec2-run-instances ami-1cdd532c -t t1.micro --region us-west-2 --key nprapps``
* Get server DNS name: ``ec2-describe-instances --region us-west-2 $INSTANCE_ID`` (keep running until available)

Configuring a server
--------------------

Creating a new cron/basic server:

* Pull current keys for a iver server: ```scp ubuntu@cron-staging.nprapps.org:~/.ssh/authorized_keys .``
* Push authorized keys to the new server: ``scp -i ~/.ssh/nprapps.pem authorized_keys ubuntu@$SERVER_DNS_NAME:~/.ssh/``
* SSH in: ``ssh ubuntu@$SERVER_DNS_NAME``
* Fetch setup script: ``wget https://raw.github.com/nprapps/servers/master/setup_cron.sh``
* Run setup script: ``sudo bash setup_cron.sh``
* Type in configuration values and wait for script to complete. The server will reboot.
* SSH in again (see above)
* ``rm setup_cron.sh``

**TODO**

* Install/generate .s3cfg
* Configure Scout
