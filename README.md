NPR Apps Servers
================

These scripts are designed to turn a brand new Ubuntu 12.04 server image (``ami-1cdd532c`` for ``us-west-2``) into a fully functional server.

It is expected that AMIs will be taken of each server and used for routine spin-ups, but these scripts allow us to quickly modify the basic recipe. (And track changes.)

Remember: **never make a baked AMI public.**

Cron
----

Creating a new cron/basic server:

* ``ssh -i ~/.ssh/nprapps.pem ubuntu@$NEW_SERVER``
* ``wget https://raw.github.com/nprapps/servers/master/setup_cron.sh``
* ``chmod +x setup_cron.sh``
* ``sudo bash setup_cron.sh``
* Type in configuration values and wait for script to complete.
* ``rm setup_cron.sh``

