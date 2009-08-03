# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext

import djanjinja
from djanjinja.views import context_to_dict


def plain(request):
    """Renders a template with no context and returns it in a response."""
    
    template = djanjinja.get_template('plain.txt')
    content = template.render()
    return HttpResponse(content=content)


def context(request):
    """Renders a template with a context and returns it in a response."""
    
    template = djanjinja.get_template('context.txt')
    content = template.render({'a': 1, 'b': 2})
    return HttpResponse(content=content)


def req_context(request):
    """Renders a template with a ``RequestContext`` and returns a repsonse."""
    
    template = djanjinja.get_template('req_context.txt')
    content = template.render(context_to_dict(RequestContext(request)))
    return HttpResponse(content=content)
