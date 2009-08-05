# -*- coding: utf-8 -*-

"""
Django-compatible Jinja2 Environment and helpers.

This module contains a subclass of ``jinja2.Environment`` and several other
functions which help use Jinja2 from within your Django projects.
"""

from functools import wraps
try:
    set
except NameError:
    from sets import Set as set

import jinja2


TEMPLATE_ENVIRONMENT = None


class Environment(jinja2.Environment):
    
    """An environment with decorators for filters, functions and tests."""
    
    def __init__(self, *args, **kwargs):
        super(Environment, self).__init__(*args, **kwargs)
        # Add a `set()` attribute which stores the loaded bundles.
        self.loaded_bundles = set()
    
    def load(self, app_label, bundle_name, reload=False):
        """Load the specified bundle into this environment."""
        
        from djanjinja import loader
        
        # Returns the loaded bundle.
        return loader.load(
            app_label, bundle_name, environment=self, reload=reload)
    
    def copy(self):
        """Create a copy of the environment."""
        
        copy = self.overlay()
        for attr in ['loaded_bundles', 'globals', 'filters', 'tests']:
            setattr(copy, attr, getattr(self, attr).copy())
        
        return copy
    
    # pylint: disable-msg=C0111
    def adder(attribute, wrapper, name, docstring):
        
        """
        Generate decorator methods for adding filters, functions and tests.
        
        Note that this function is not a method; it is deleted before the end
        of the class definition and is only used to generate the decorator
        methods. It helps to remove a lot of boilerplate.
        """
        
        def adder_(self, function, name=None):
            """Add the function to the environment with wrappers, etc."""
            
            key = name or function.__name__
            value = wrapper and wrapper(function) or function
            getattr(self, attribute)[key] = value
            return function
        
        def decorator(self, *args, **kwargs):
            """Boilerplate which allows both normal calling and decoration."""
            
            def wrapper(*args):
                return adder_(self, *args, **kwargs)
            if args:
                return wrapper(*args)
            return wrapper
        
        decorator.__name__ = name
        decorator.__doc__ = docstring
        return decorator
    
    ## Simple
    
    filter = adder('filters', None, 'filter',
        'Decorate a function as a simple template filter.')
    
    test = adder('tests', None, 'test',
        'Decorate a function as a simple template test.')
    
    function = adder('globals', None, 'function',
        'Decorate a function as a simple global template function.')
        
    ## Environment
    # Note that environment- and context-tests are not supported by Jinja2.
    
    envfilter = adder('filters', jinja2.environmentfilter, 'envfilter',
        'Decorate a function as an environment filter.')
    
    envfunction = adder('globals', jinja2.environmentfunction, 'envfunction',
        'Decorate a function as a global environment function.')
    
    ## Context
    
    ctxfilter = adder('filters', jinja2.contextfilter, 'ctxfilter',
        'Decorate a function as a context filter.')
    
    ctxfunction = adder('globals', jinja2.contextfunction, 'ctxfunction',
        'Decorate a function as a global context function.')
    
    # Clean up the namespace. Also, without this, `type` will try to convert
    # `adder()` into a method. Which it most certainly is not.
    del adder


def get_template_source(name):
    
    """
    Interface with Django to load the source for a given template name.
    
    This function is a simple wrapper around
    ``django.template.loader.find_template_source()`` to support the behaviour
    expected by the ``jinja2.FunctionLoader`` loader class. It requires Django
    to be configured (i.e. the settings need to be loaded).
    """
    
    from django.template import loader
    # `loader.find_template_source()` returns a 2-tuple of the source and a
    # `LoaderOrigin` object. 
    source = loader.find_template_source(name)[0]
    
    # `jinja2.FunctionLoader` expects a triple of the source of the template,
    # the name used to load it, and a 0-ary callable which will return whether
    # or not the template needs to be reloaded. The callable will only ever be
    # called if auto-reload is on. In this case, we'll just assume that the
    # template does need to be reloaded.
    return (source, name, lambda: False)


def bootstrap():
    """Load the TEMPLATE_ENVIRONMENT global variable."""
    
    from django.conf import settings
    if not settings.configured:
        # At least this will make it work, even if it's using the defaults.
        settings.configure()
    
    from djanjinja import bccache
    from djanjinja.extensions.cache import CacheExtension
    
    # Get the bytecode cache object.
    bytecode_cache = bccache.get_cache()
    
    default_extensions = set([
        'jinja2.ext.do', 'jinja2.ext.loopcontrols', CacheExtension])
    if getattr(settings, 'USE_I18N', False):
        default_extensions.add('jinja2.ext.i18n')
    
    extensions = getattr(settings, 'JINJA_EXTENSIONS', []) + list(
        default_extensions)
    
    # Set up global `TEMPLATE_ENVIRONMENT` variable.
    global TEMPLATE_ENVIRONMENT
    
    TEMPLATE_ENVIRONMENT = Environment(
        loader=jinja2.FunctionLoader(get_template_source),
        auto_reload=getattr(settings, 'DEBUG', True),
        bytecode_cache=bytecode_cache, extensions=extensions)
    
    if getattr(settings, 'USE_I18N', False):
        # The `django.utils.translation` module behaves like a singleton of
        # `gettext.GNUTranslations`, since it exports all the necessary
        # methods.
        from django.utils import translation
        # pylint: disable-msg=E1101
        TEMPLATE_ENVIRONMENT.install_gettext_translations(translation)
    
    bundles = getattr(settings, 'DJANJINJA_BUNDLES', [])
    for bundle_specifier in bundles:
        app_label, bundle_name = bundle_specifier.rsplit('.', 1)
        TEMPLATE_ENVIRONMENT.load(app_label, bundle_name)


def is_safe(function):
    """Decorator which declares that a function returns safe markup."""
    
    @wraps(function)
    def safe_wrapper(*args, **kwargs):
        """Wraps the output of the function as safe markup."""
        
        # All this wrapper does is to wrap the output of the function with
        # `jinja2.Markup`, which declares to the template that the string is
        # safe.
        result = function(*args, **kwargs)
        if not isinstance(result, jinja2.Markup):
            return jinja2.Markup(result)
        return result
    
    return safe_wrapper
