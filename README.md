NPR Apps Servers
================

Spinning up a cron/basic server:

* Create new Ubuntu 12.04 server--``ami-1cdd532c`` for ``us-west-2`` (Oregon).
* ``ssh -i ~/.ssh/nprapps.pem ubuntu@$SERVER_IP``
* ``wget https://raw.github.com/nprapps/servers/master/setup_cron.sh``
* ``chmod +x setup_cron.sh``
* ``sudo bash setup_cron.sh``
* Type in configuration values and wait for script to complete.
* ``rm setup_cron.sh``

