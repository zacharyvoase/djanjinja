# -*- coding: utf-8 -*-

"""Views which use DjanJinja shortcut functions to render templates."""

from django.template import RequestContext

from djanjinja.views import context_to_dict, render_to_response


def plain(request):
    """Renders a template with no context directly to a response."""
    
    return render_to_response('plain.txt')


def context(request):
    """Renders a template with a context directly to a response."""
    
    return render_to_response('context.txt', {'a': 1, 'b': 2})


def req_context(request):
    """Renders a template with a ``RequestContext`` directly to a response."""
    
    return render_to_response('req_context.txt',
        context_to_dict(RequestContext(request)))


def middleware(request):
    """Renders a template with ``request.Context`` using middleware."""
    
    return request.Context({'a': 1, 'b': 2}).render_response('middleware.txt')