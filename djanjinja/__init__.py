# -*- coding: utf-8 -*-

"""djanjinja - A reusable Django app to use Jinja2 templates from Django."""

from djanjinja import environment
from djanjinja.environment import is_safe


__all__ = [
    'bccache',
    'bundles',
    'environment',
    'extensions',
    'generic',
    'handlers',
    'loader',
    'middleware',
    'views',
]

__version__ = '0.7'


def get_environment():
    """Return the template environment, bootstrapping if necessary."""
    
    if not environment.TEMPLATE_ENVIRONMENT:
        environment.bootstrap()
    return environment.TEMPLATE_ENVIRONMENT

# Shorthand alias for `get_environment()`.
get_env = get_environment


def get_template(template_name):
    """Return the specified template."""
    
    return get_env().get_template(template_name)
