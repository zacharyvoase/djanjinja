# -*- coding: utf-8 -*-

"""Port of django.contrib.humanize to Jinja2."""

from django.contrib.humanize.templatetags import humanize
from djanjinja.loader import Bundle


bundle = Bundle()
# All of the humanize filters are plain functions too, and Django's way of
# storing filters is very similar; we just update our bundle's `filters`
# attribute using humanize's register.
bundle.filters.update(humanize.register.filters)
