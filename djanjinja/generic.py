# -*- coding: utf-8 -*-

"""
Generic views for Django which use Jinja2 instead.

At the moment this module only contains ``direct_to_template``. Eventually it
may house some more useful generic views, which have been made to use Jinja2
instead of Django's built-in template language.
"""

import mimetypes

from djanjinja.middleware import RequestContextMiddleware
from djanjinja.views import DEFAULT_CONTENT_TYPE


def direct_to_template(request, template=None, extra_context=None,
    mimetype=None, *args, **kwargs):
    
    """
    A generic view, similar to that of the same name provided by Django.
    
    Please consult the documentation for Django's
    ``django.views.generic.simple.direct_to_template`` generic view. This
    function exports an identical calling signature, only it uses the Jinja2
    templating system instead.
    """
    
    # Ensure the request has a `Context` attribute. This means the middleware
    # does not have to be installed.
    if not hasattr(request, 'Context'):
        RequestContextMiddleware.process_request(request)
    
    # Build the context, optionally accepting additional context values.
    context = request.Context(dict=(extra_context or {}))
    
    # Build the `params` variable from the parameters passed into the view
    # from the URLconf.
    params = kwargs.copy()
    for i, value in enumerate(args):
        params[i] = value
    context['params'] = params
    
    # Ensure the mimetype is sensible; if not provided, it will be inferred
    # from the name of the template. If that fails, fall back to the default.
    if not mimetype:
        mimetype = mimetypes.guess_type(template)[0] or DEFAULT_CONTENT_TYPE
    
    return context.render_response(template, mimetype=mimetype)
