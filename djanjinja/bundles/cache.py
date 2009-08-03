# -*- coding: utf-8 -*-

"""Add the Django cache object to the global template variables."""

from django.core import cache

from djanjinja.loader import Bundle


bundle = Bundle()
bundle.globals['cache'] = cache.cache