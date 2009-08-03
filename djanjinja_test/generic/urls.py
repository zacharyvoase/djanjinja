# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('djanjinja.generic',
    url(r'^plain/$', 'direct_to_template', {'template': 'plain.txt'},
        name='generic-plain'),
    url(r'^context/$', 'direct_to_template',
        {'template': 'context.txt', 'extra_context': {'a': 1, 'b': 2}},
        name='generic-context'),
    url(r'^req_context/$', 'direct_to_template',
        {'template': 'req_context.txt'}, name='generic-req_context')
)