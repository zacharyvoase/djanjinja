# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('djanjinja_test.shortcuts.views',
    url(r'^plain/$', 'plain', name='shortcuts-plain'),
    url(r'^context/$', 'context', name='shortcuts-context'),
    url(r'^req_context/$', 'req_context', name='shortcuts-req_context'),
    url(r'^middleware/$', 'middleware', name='shortcuts-middleware'),
)