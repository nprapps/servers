NPR Apps Servers
=========================

* [About NPR Apps servers](#about-servers)
* [Creating servers](#creating-servers)
* [Cron](#cron)
* [Configure the project](#configure-the-project)
* [Install requirements](#install-requirements)
* [Deploy to EC2](#deploy-to-ec2)

About Servers
--------------

These scripts are designed to turn a brand new Ubuntu 12.04 server image into a fully functional server.

It is expected that AMI snapshots will be taken of each server and used for routine spin-ups, but these scripts allow us to quickly modify the basic recipe. (And track changes.)

Remember: **never make a baked AMI public.**

Creating servers
-----------------

If creating servers with the web console isn't fast enough for you, then you can create servers from the command line with the EC2 API tools. Install them with:

``brew install ec2-api-tools``

At the end of the installation a set of environment variables to be set will be printed. Be sure to add these to your ``~/.bash_profile``. You will also need to download a private key and X.509 certificate from AWS. Update the ``EC2_PRIVATE_KEY`` and ``EC2_CERT`` environment variables to point to these files.

Once configured you can create a new server from your command line:

* Create server: ``ec2-run-instances ami-1cdd532c -t t1.micro --region us-west-2 --key nprapps``
* Get server DNS name: ``ec2-describe-instances --region us-west-2 $INSTANCE_ID`` (keep running until available)

Cron
-----

Creating a new cron/basic server:

* Install list of live SSH keys: ``scp -i ~/.ssh/nprapps.pem ubuntu@cron-staging.nprapps.org:~/.ssh/authorized_keys
 ubuntu@$SERVER_DNS_NAME:~/.ssh/``
* SSH in: ``ssh ubuntu@$SERVER_DNS_NAME``
* Fetch setup script: ``wget https://raw.github.com/nprapps/servers/master/setup_cron.sh``
* Run setup script: ``sudo bash setup_cron.sh``
* Type in configuration values and wait for script to complete. The server will reboot.
* SSH in again (see above)
* ``rm setup_cron.sh``

**TODO**

Install/generate .s3cfg

Configure the project
---------------------

Edit ``app_config.py`` and update ``PROJECT_NAME``, ``DEPLOYED_NAME``, ``REPOSITORY_NAME`` any other relevant configuration details.

Install requirements
--------------------

Make a virtualenv and install the project requirements:

```
cd servers
mkvirtualenv servers
pip install -r requirements.txt
```

Add Nginx configuration
-----------------------
Add your configuration file to the `nginx/sites-available/` folder. Use the `static` and `status` configurations as examples.

***Do not deploy application-specific files with this app*** Application-specific files should be added via the application's `fab deploy` command.


Deploy to EC2
-------------

Deploy your new server configurations to EC2.

```
fab <branch> <destination> deploy
```

You can also remove any deployed configurations from EC2.

```
fab <destination> shiva_the_destroyer
```
