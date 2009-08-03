# -*- coding: utf-8 -*-

"""Tests for views which render templates which use the caching extras."""

from django.test import TestCase

import djanjinja


CACHE_GLOBAL_RESPONSE = u'value'


class CacheTest(TestCase):
    
    def test_global(self):
        response = self.client.get('/cache/global/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, CACHE_GLOBAL_RESPONSE)
        
    def test_fragment(self):
        """Tests the fragment caching extension."""
        
        # A singleton which stores the number of times its `call()` method has
        # been called.
        # pylint: disable-msg=C0103
        class call_state(object):
            called = 0
            
            @classmethod
            def call(cls):
                cls.called += 1
        
        template = djanjinja.get_template('cache_fragment.txt')
        # In the beginning, `called` will be 0.
        self.assertEqual(call_state.called, 0)
        
        # After rendering once, `called` will be 1.
        template.render({'call_state': call_state})
        self.assertEqual(call_state.called, 1)
        
        # If fragment caching is working correctly, the output of the previous
        # render should be stored and the `call()` method should not be called
        # again.
        template.render({'call_state': call_state})
        self.assertEqual(call_state.called, 1)