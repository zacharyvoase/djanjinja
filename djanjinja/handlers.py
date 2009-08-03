# -*- coding: utf-8 -*-

"""Replacement for the default Django 404/500 exception handlers."""

from djanjinja.views import RequestContext, render_to_response


def page_not_found(request, template_name='404.html'):
    
    """
    404 (page not found) handler which uses Jinja2 to render the template.
    
    The default template is ``404.html``, and its context will contain
    ``request_path`` (the path of the requested URL) and any additional
    parameters provided by the registered context processors (this view uses
    ``RequestContext``).
    """
    
    context = RequestContext(request, {'request_path': request.path})
    response = context.render_response(template_name)
    response.status_code = 404
    return response


def server_error(request, template_name='500.html'):
    
    """
    500 (server error) handler which uses Jinja2 to render the template.
    
    The default template is ``500.html``, and it will be rendered with a
    completely empty context. This is to prevent further exceptions from being
    raised.
    """
    
    return render_to_response(template_name)
