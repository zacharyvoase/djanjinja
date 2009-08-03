# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('djanjinja_test.cache.views',
    url(r'^global/$', 'global_', name='cache-global'),
)
