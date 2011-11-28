# -*- coding: utf-8 -*-
"""
    rediscache
    ~~~~~~~~~~~~~~

    Adds cache support to your application.

    :copyright: (c) 2011 by Chronos.
    :license: BSD, see LICENSE for more details
"""
import redis
import cPickle

from StringIO import StringIO
from functools import wraps
from flask import request, current_app


#: Cache Object
################

class Cache(object):
    """
    This class is used to control the cache objects.
    """

    def __init__(self, app=None):
        self.cache = None

        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        "This is used to initialize cache with your app object"
        '''
        app.config.setdefault('CACHE_REDIS_SERVERS', 'localhost')
        app.config.setdefault('CACHE_REDIS_PORT', 6379)
        app.config.setdefault('CACHE_REDIS_DB', 0)
        '''
        self.app = app
        self._set_cache()

    def _set_cache(self):
        self.cache = redis.Redis(host=self.app.config['CACHE_REDIS_SERVERS'],
                                port=self.app.config['CACHE_REDIS_PORT'],
                                db=self.app.config['CACHE_REDIS_DB'])

    def get(self, key):
        "返回key对应的value"
        value = self.cache.get(key)
        if value == None:
            return None
        return cPickle.load(StringIO(value))

    def set(self, key, value, timeout=None):
        "设定缓存值"
        stringio = StringIO()
        cPickle.dump(value,stringio)
        stringio.seek(0)
        self.cache.set(key, stringio.read())
        if timeout:
            self.cache.expire(key, timeout)

    def delete(self, key):
        "清除key对应的缓存"
        self.cache.delete(key)
        
    def deletes(self, keys=[], pattern=None):
        "批量删除"
        if pattern:
            keys = self.keys(pattern)
            
        for key in keys:
            self.cache.delete(key)
    
    def keys(self, pattern):
        "返回匹配的key集合"
        return self.cache.keys(pattern)
        
    def cached(self, timeout=None, key_prefix='%s', unless=None):
        """
        Decorator. Use this to cache a function. By default the cache key
        is `view/request.path`. You are able to use this decorator with any
        function by changing the `key_prefix`. If the token `%s` is located
        within the `key_prefix` then it will replace that with `request.path`

        Example::

            # An example view function
            @cache.cached(timeout=50)
            def big_foo():
                return big_bar_calc()

            # An example misc function to cache.
            @cache.cached(key_prefix='MyCachedList')
            def get_list():
                return [random.randrange(0, 1) for i in range(50000)]

        .. code-block:: pycon

            >>> my_list = get_list()
            
        .. note::
        
            You MUST have a request context to actually called any functions
            that are cached.

        :param timeout: Default None. If set to an integer, will cache for that
                        amount of time. Unit of time is in seconds.
        :param key_prefix: Default 'view/%(request.path)s'. Beginning key to .
                           use for the cache key.
        :param unless: Default None. Cache will *always* execute the caching
                       facilities unless this callable is true.
                       This will bypass the caching entirely.
        """

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                #: Bypass the cache entirely.
                if callable(unless) and unless() is True:
                    return f(*args, **kwargs)

                if '%s' in key_prefix:
                    cache_key = key_prefix % request.path
                else:
                    cache_key = key_prefix
                
                rv = self.get(cache_key)
                if rv is None:
                    rv = f(*args, **kwargs)
                    self.set(cache_key, rv, timeout=timeout)
                return rv
            return decorated_function
        return decorator
