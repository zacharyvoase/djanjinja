# -*- coding: utf-8 -*-

"""
djanjinja.middleware - Helpful middleware for using Jinja2 from Django.

This module contains middleware which helps you use Jinja2 from within your
views. At the moment it only contains ``RequestContextMiddleware``, but may
expand in future.
"""

from djanjinja.views import RequestContext


class RequestContextMiddleware(object):
    
    """Attach a special ``RequestContext`` class to each request object."""
    
    @staticmethod
    def process_request(request):
        
        """
        Attach a special ``RequestContext`` subclass to each request object.
        
        This is the only method in the ``RequestContextMiddleware`` Django
        middleware class. It attaches a ``RequestContext`` subclass to each
        request as the ``Context`` attribute. This subclass has the request
        object pre-specified, so you only need to use ``request.Context()`` to
        make instances of ``django.template.RequestContext``.
        
        Consult the documentation for ``djanjinja.views.RequestContext`` for
        more information.
        """
        
        request.Context = RequestContext.with_request(request)
