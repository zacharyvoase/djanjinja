# -*- coding: utf-8 -*-

"""A Jinja2 bytecode cache which uses the Django caching framework."""

import jinja2


class B64CacheClient(object):
    
    """
    A wrapper for the Django cache client which Base64-encodes everything.
    
    This wrapper is needed to use the Django cache with Jinja2. Because Django
    tries to store/retrieve everything as Unicode, it makes it impossible to
    store binary data. Since Jinja2 uses marshal to store bytecode, we need to
    Base64-encode the binary data and then we can send that into and get that
    out of the Django cache.
    """
    
    def __init__(self, cache):
        self.cache = cache
    
    def get(self, key):
        """Fetch a key from the cache, base64-decoding the result."""
        data = self.cache.get(key)
        if data is not None:
            return data.decode('base64')
    
    def set(self, key, value, timeout=None):
        """Set a value in the cache, performing base64 encoding beforehand."""
        if timeout is not None:
            self.cache.set(key, value.encode('base64'), timeout)
        else:
            self.cache.set(key, value.encode('base64'))


def get_cache():
    """Get a Jinja2 bytecode cache which uses the configured Django cache."""
    
    from django.conf import settings
    from django.core import cache
    
    cache_backend = cache.parse_backend_uri(settings.CACHE_BACKEND)[0]
    memcached_client = None
    
    if cache_backend == 'memcached':
        # We can get the actual memcached client object itself. This will
        # avoid the Django problem of storing binary data (as Django tries to
        # coerce everything to Unicode).
        
        # Here, we look for either `cache.cache._cache` or
        # `cache.cache._client`; I believe there is some discrepancy between
        # different versions of Django and where they put this.
        memcached_client = getattr(
            cache.cache, '_cache', getattr(cache.cache, '_client', None))
    
    memcached_client = memcached_client or B64CacheClient(cache.cache)
    
    return jinja2.MemcachedBytecodeCache(memcached_client)
