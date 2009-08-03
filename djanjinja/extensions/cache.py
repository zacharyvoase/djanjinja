# -*- coding: utf-8 -*-

"""
A Jinja2 template tag for fragment caching.

This extension, copied mainly from the Jinja2 documentation on extensions,
adds a ``{% cache %}`` tag which permits fragment caching, much like that in
the native Django templating language.

Usage is as follows:
    
    {% cache "cache_key", 3600 %}
        ...
    {% endcache %}

This will cache the fragment between ``cache`` and ``endcache``, using the
cache key ``"cache_key"`` and with a timeout of 3600 seconds.

More complex cache keys can be specified by passing in a sequence (such as a
list or tuple) of items. The entire sequence must be 'dumpable' using the
standard ``marshal`` module in Python. For example:
    
    {% cache ("article", article.id), 3600 %}
        ...
    {% endcache %}

To generate the key, the tuple is marshalled, the SHA1 hash of the resulting
string is taken and base64-encoded, with newlines and padding stripped, and
this is appended to the string ``jinja_frag_``. For more information, consult
the code (located in ``djanjinja/extensions/cache.py``).
"""

import hashlib
import marshal

from jinja2 import nodes
from jinja2.ext import Extension


class CacheExtension(Extension):
    
    """Fragment caching using the Django cache system."""
    
    tags = set(['cache'])
    cache_key_format = 'jinja_frag_%(hash)s'
    
    def __init__(self, environment):
        super(CacheExtension, self).__init__(environment)
        
        # Extend the environment with the default cache key prefix.
        environment.extend(cache_key_format=self.cache_key_format)
        
    def parse(self, parser):
        """Parse a fragment cache block in a Jinja2 template."""
        
        # The first parsed token will be 'cache', so we ignore that but keep
        # the line number to give to nodes we create later.
        lineno = parser.stream.next().lineno
        
        # This should be the cache key.
        args = [parser.parse_expression()]
        
        # This will check to see if the user provided a timeout parameter
        # (which would be separated by a comma).
        if parser.stream.skip_if('comma'):
            args.append(parser.parse_expression())
        else:
            args.append(nodes.Const(None))
        # Here, we parse up to {% endcache %} and drop the needle, which will
        # be the `endcache` tag itself.
        body = parser.parse_statements(['name:endcache'], drop_needle=True)
        
        # Now return a `CallBlock` node which calls the `_cache` method on the
        # extension.
        return nodes.CallBlock(
            self.call_method('_cache', args), [], [], body
        ).set_lineno(lineno)
    
    def _cache(self, parameters, timeout, caller):
        """Helper method for fragment caching."""
        
        # This is lazily loaded so that it can be set up without Django. If
        # you try to use it without Django, it will just render the fragment
        # as usual.
        try:
            from django.core import cache
        except ImportError:
            # `caller()` will render whatever is between {% cache %} and
            # {% endcache %}.
            return caller()
        
        key = self._generate_key(parameters)
        
        # If the fragment is cached, return it. Otherwise, render it, set the
        # key in the cache, and return it.
        retrieved_value = cache.cache.get(key)
        if retrieved_value is not None:
            return retrieved_value
        
        value = caller()
        cache.cache.set(key, value, timeout)
        return value
        
    def _generate_key(self, parameters):
        """Generate a cache key from some parameters (maybe a sequence)."""
        
        # Marshal => Hash => Prefix should generate a unique key for each
        # set of parameters which is the same for equal parameters.
        # Essentially, this is a 1:1 mapping.
        serialized = marshal.dumps(parameters)
        digest = (hashlib.sha1(serialized)
            .digest()
            .encode('base64')
            .rstrip('\r\n='))
        
        return self.environment.cache_key_format % {'hash': digest}