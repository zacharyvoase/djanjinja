# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('djanjinja_test.simple.views',
    url(r'^plain/$', 'plain', name='simple-plain'),
    url(r'^context/$', 'context', name='simple-context'),
    url(r'^req_context/$', 'req_context', name='simple-req_context'),
)
