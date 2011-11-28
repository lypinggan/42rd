#!/bin/bash
apt-get install python-setuptools
apt-get install libmysqld-dev
apt-get install libmysqlclient-dev
apt-get install python-dev
easy_install mysql-python
easy_install Flask==0.6
easy_install Flask-Cache
easy_install Flask-SQLAlchemy
easy_install Flask-Principal
easy_install Flask-WTF
easy_install Flask-Mail
easy_install Flask-Testing
easy_install Flask-Script
easy_install Flask-OpenID
easy_install Flask-Babel
easy_install Flask-Themes
easy_install sqlalchemy
easy_install markdown
easy_install feedparser
easy_install blinker
easy_install nose

#apt-get install python2.6-dev libxml2-dev
#cd /home/lyping/soft/
#wget http://projects.unbit.it/downloads/uwsgi-0.9.7.1.tar.gz
#tar zxvf uwsgi-0.9.7.1.tar.gz
#cd uwsgi-0.9.7.1
#make -f Makefile.Py26
#cp uwsgi /usr/bin
