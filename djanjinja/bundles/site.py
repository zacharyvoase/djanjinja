# -*- coding: utf-8 -*-

"""Contains definitions for working with your Django site itself."""

from djanjinja.loader import Bundle


bundle = Bundle()


@bundle.function
def url(name, *args, **kwargs):
    """A simple wrapper around ``django.core.urlresolvers.reverse``."""
    
    from django.core.urlresolvers import reverse    
    return reverse(name, args=args, kwargs=kwargs)


@bundle.function
def setting(name, default=None):
    """Get the value of a particular setting, defaulting to ``None``."""
    
    from django.conf import settings
    return getattr(settings, name, default)