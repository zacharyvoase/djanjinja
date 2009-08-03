# -*- coding: utf-8 -*-

from django.conf.urls.defaults import include, patterns


urlpatterns = patterns('',
    (r'^simple/', include('djanjinja_test.simple.urls')),
    (r'^shortcuts/', include('djanjinja_test.shortcuts.urls')),
    (r'^generic/', include('djanjinja_test.generic.urls')),
    (r'^cache/', include('djanjinja_test.cache.urls')),
)


handler404 = 'djanjinja.handlers.page_not_found'
handler500 = 'djanjinja.handlers.server_error'