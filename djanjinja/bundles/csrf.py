# -*- coding: utf-8 -*-

"""Add a helper to the context for rendering CSRF tokens."""

import django
from django.core.exceptions import ImproperlyConfigured
from djanjinja.loader import Bundle


bundle = Bundle()

if django.VERSION >= (1, 2): # CSRF changed in Django v1.2+
    @bundle.ctxfunction
    def csrf_token(context):
        token = context.get('csrf_token', None)
        if token:
            if token == 'NOTPROVIDED':
                return Markup(u'')
            return Markup(
                u'<div style="display: none;">'
                    u'<input type="hidden" name="csrfmiddlewaretoken" value="%s" />'
                u'</div>' % (token,))
        
        if 'django.core.context_processors.csrf' in settings.TEMPLATE_CONTEXT_PROCESSORS:
            raise ImproperlyConfigured(
                "csrf_token() was used in a template, but a CSRF token was not "
                "present in the context. This is usually caused by not using "
                "RequestContext.")
        else:
            raise ImproperlyConfigured(
                "csrf_token() was used in a template, but a CSRF token was not "
                "present in the context. You need to add "
                "'django.core.context_processors.csrf' to the "
                "TEMPLATE_CONTEXT_PROCESSORS setting, and use RequestContext.")
