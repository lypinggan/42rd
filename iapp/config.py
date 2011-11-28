# -*- coding: utf-8 -*-
'''
配置文件
'''
from iapp import views

class DefaultConfig(object):
    
    DEBUG = True

    # change this in your production settings !!!

    SECRET_KEY = "secret"

    # keys for localhost. Change as appropriate.

    RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
    #MYSQL连接
    SQLALCHEMY_DATABASE_URI = "mysql://root:lyping!@#@localhost/42ic?charset=utf8"

    SQLALCHEMY_ECHO = True#False

    MAIL_DEBUG = DEBUG

    ADMINS = ()

    ADMINS = ('11939053@qq.com',)

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = '42rd.com'
    MAIL_PASSWORD = 'lypingb7y4g3'
    DEFAULT_MAIL_SENDER = '42rd.com@gmail.com'

    
    #ACCEPT_LANGUAGES = ['en_gb', 'zh']
    ACCEPT_LANGUAGES = ['en_gb', 'fi']
    BABEL_DEFAULT_LOCALE = 'zh'
    BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'

    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'


    CACHE_TYPE = "simple"
    CACHE_MEMCACHED_SERVERS = "127.0.0.1:12000"
    CACHE_KEY_PREFIX = "cache"
    CACHE_DEFAULT_TIMEOUT = 300

	#Í³¼Æ
    GOOGLE_TRACKING_CODE = 'UA-24331000-1'
    #cache
    CACHE_REDIS_SERVERS = 'localhost'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_DB = 0
    #路径
    #网站文件路径
    WEB_PATH = '/home/lyping/data/42rd/'
    STATIC_PATH = WEB_PATH+'static/'
    IMG_PATH = WEB_PATH+'img/'
    FILE_PATH = WEB_PATH+'file/'
    
    #各种URL
    APP_URL = 'http://www.42rd.com/'
    IMG_URL = 'http://www.42rd.com/static/img/'
    FILE_URL = 'http://www.42rd.com/static/file/'
    #普通静态文件
    STATIC_DOMAIN = 'http://img1.42rd.com'
    

class TestConfig(object):

    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ECHO = False




