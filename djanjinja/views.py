# -*- coding: utf-8 -*-

"""
djanjinja.views - Utilities to help write Django views which use Jinja2.

This module contains several functions and classes to make it easier to write
views which use Jinja2. It replaces a couple of the most common Django
template-rendering shortcuts, and features an extended ``RequestContext``.
"""

from functools import partial

from django import template
from django.conf import settings
from django.http import HttpResponse

from djanjinja import get_env


DEFAULT_CONTENT_TYPE = getattr(settings, 'DEFAULT_CONTENT_TYPE', 'text/html')


class RequestContext(template.RequestContext):
    
    """A ``RequestContext`` with a pre-specified request attribute."""
    
    request = None
    
    def __init__(self, *args, **kwargs):
        # If the class has a `request` attribute which is not `None`, use that
        # to initialize the `RequestContext`.
        if self.request is not None:
            super(RequestContext, self).__init__(
                self.request, *args, **kwargs)
        else:
            # Otherwise, just act as if the normal ``RequestContext``
            # constructor was called.
            super(RequestContext, self).__init__(*args, **kwargs)
    
    @classmethod
    def with_request(cls, request):
        """Return a `RequestContext` subclass for a specified request."""
        
        # Subclasses `RequestContext` with a value for `request`, so that it
        # does not need it as an explicit request argument for initialization.
        return type(
            cls.__name__, (cls,),
            {'request': request, '__module__': cls.__module__})
    
    def render_string(self, filename):
        """Render a given template name to a string, using this context."""
        
        return render_to_string(filename, context=self)
    
    def render_response(self, filename, mimetype=DEFAULT_CONTENT_TYPE):
        """Render a given template name to a response, using this context."""
        
        return render_to_response(filename, context=self, mimetype=mimetype)


def context_to_dict(context):
    """Flattens a Django context into a single dictionary."""
    
    if not isinstance(context, template.Context):
        return context
    
    dict_out = {}
    
    # This helps us handle the order of dictionaries in the context. By
    # default, the most recent (and therefore most significant/important)
    # sub-dictionaries are at the front of the list. This means that variables
    # defined later on need to be processed last, hence the use of the
    # `reversed()` built-in.
    for sub_dict in reversed(context.dicts):
        dict_out.update(sub_dict)
    return dict_out


def render_to_string(filename, context=None, environment=None):
    """Renders a given template name to a string."""
    
    if context is None:
        context = {}
    
    if environment is None:
        environment = get_env()
    
    return environment.get_template(filename).render(
        context_to_dict(context))


def render_to_response(filename, context=None, mimetype=DEFAULT_CONTENT_TYPE,
        environment=None):
    """Renders a given template name to a ``django.http.HttpResponse``."""
    
    return HttpResponse(
        render_to_string(filename, context=context, environment=environment),
        mimetype=mimetype)


def shortcuts_for_environment(environment):
    """Returns shortcuts pre-configured for a given environment."""
    
    return (
        partial(render_to_string, environment=environment),
        partial(render_to_response, environment=environment))
