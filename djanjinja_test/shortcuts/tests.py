# -*- coding: utf-8 -*-

"""Tests for views which render templates using DjanJinja shortcuts."""

from django.test import TestCase


PLAIN_RESPONSE = 'Hello, World!'
CONTEXT_RESPONSE = 'a = 1; b = 2'
REQ_CONTEXT_RESPONSE = 'user.is_anonymous() => True'
MIDDLEWARE_RESPONSE = 'anonymous, a1, b2'


class ShortcutsTest(TestCase):
    
    def test_plain(self):
        response = self.client.get('/shortcuts/plain/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, PLAIN_RESPONSE)
    
    def test_context(self):
        response = self.client.get('/shortcuts/context/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, CONTEXT_RESPONSE)
    
    def test_req_context(self):
        response = self.client.get('/shortcuts/req_context/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, REQ_CONTEXT_RESPONSE)
    
    def test_middleware(self):
        response = self.client.get('/shortcuts/middleware/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, MIDDLEWARE_RESPONSE)