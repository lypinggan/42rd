#!/bin/bash
uwsgi -s /var/run/42ic.com.socket -M -p 2 -t 90 -R 1000 -d /home/wwwlogs/42ic.com.log --vhost --chmod-socket=666
/etc/init.d/redis-server start

#/usr/local/bin/redis-server
