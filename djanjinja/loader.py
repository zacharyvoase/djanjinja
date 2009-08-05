# -*- coding: utf-8 -*-

"""Utilities for loading definitions from reusable Django apps."""

import copy

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from djanjinja import get_env
from djanjinja.environment import Environment


class Bundle(object):
    
    """
    Store a bunch of tests, filters and functions from a single app.
    
    Instances of the ``Bundle`` class store tests, filters and functions in an
    internal register that can then be lazily merged with the Jinja2
    environment later on. It is used when apps want to define a number of
    utilities for lazy loading from template code, typically using the
    ``{% load %}`` template tag defined in djanjinja.extensions.bundles.
    
    Essentially, a bundle is just an environment without the templating and
    loading parts. They can be pushed onto another environment, which will
    return a new environment with a new set of filters, globals and tests but
    all the other attributes from the original environment.
    """
    
    TYPES = (
        'test',
        'filter', 'ctxfilter', 'envfilter',
        'function', 'ctxfunction', 'envfunction'
    )
    
    # Set these attributes now, to prevent pylint from flagging errors later.
    test = None
    filter = None
    ctxfilter = None
    envfilter = None
    function = None
    ctxfunction = None
    envfunction = None
    
    def __init__(self):
        self.filters = {}
        self.globals = {}
        self.tests = {}
    
    def merge_into(self, environment=None):
        """Push this bundle onto the environment, returning a new env."""
        
        if environment is None:
            environment = get_env()
        
        for attr in ['globals', 'filters', 'tests']:
            getattr(environment, attr).update(getattr(self, attr))
        
        return environment
    
    
    # Dynamically create decorators for each type.
    for type in TYPES:
        # We get the attribute from the `Environment` class itself because it
        # will be an unbound method at this point.
        # `im_func` is the underlying function definition. Within this
        # definition, `self` has no special meaning, so by copying it here
        # we can essentially repurpose the same method for this class. It's
        # actually similar to a mixin.
        vars()[type] = copy.copy(getattr(Environment, type).im_func)
        
        # Clean up ``type`` from the namespace.
        del type


def get_bundle(app_label, bundle_name):
    
    """
    Loads the bundle with a given name for a specific app.
    
    First, we import the app. Then, we look in the ``bundles`` sub-module for
    the specified bundle name. If the given name is a top-level attribute of
    ``bundles``, we use that. Otherwise, we try to import a submodule of
    ``bundles`` with that name and look for a ``bundle`` attribute in that
    submodule.
    
    Note that this function only retrieves the bundle; it does not insert it
    into the environment. To do this in one step, use the ``load()`` function
    in this module.
    """
    
    from django.conf import settings
    
    # Load the app (this is a plain Python module).
    app, app_name = None, ''
    for full_app_name in settings.INSTALLED_APPS:
        if app_label in (full_app_name, full_app_name.split('.')[-1]):
            app = import_module(full_app_name)
            app_name = full_app_name
            break
    if not (app and app_name):
        raise ImproperlyConfigured(
            'App with label %r not found' % (app_label,))
    
    # Try to find the bundles sub-module. Having this separate allows us to
    # provide a more detailed exception message.
    try:
        bundles = import_module('.bundles', package=app_name)
    except ImportError:
        raise ImproperlyConfigured(
            'App %r has no `bundles` module' % (app_name,))
    
    # Now load the specified bundle name. First we look to see if it is a top-
    # level attribute of the bundles module:
    if hasattr(bundles, bundle_name):
        bundle = getattr(bundles, bundle_name)
        if isinstance(bundle, Bundle):
            return bundle
    
    try:
        bundle_mod = import_module(
            '.' + bundle_name, package=(app_name + '.bundles'))
    except ImportError:
        raise ImproperlyConfigured(
            'Could not find bundle %r in app %r' % (bundle_name, app_name))
    
    if hasattr(bundle_mod, 'bundle'):
        return getattr(bundle_mod, 'bundle')
    raise ImproperlyConfigured(
        "Module '%s.bundles.%s' has no `bundle` attribute" % (
            app_name, bundle_name))


def load(app_label, bundle_name, environment=None, reload=False):
    """Load a specified bundle into an/the environment."""
    
    if environment is None:
        environment = get_env()
    
    bundle = get_bundle(app_label, bundle_name)
    if (bundle not in environment.loaded_bundles) or reload:
        bundle.merge_into(environment)
        environment.loaded_bundles.add(bundle)
    return bundle