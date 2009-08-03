# -*- coding: utf-8 -*-

"""Tests for views which render templates using the generic views."""

from django.test import TestCase


PLAIN_RESPONSE = 'Hello, World!'
CONTEXT_RESPONSE = 'a = 1; b = 2'
REQ_CONTEXT_RESPONSE = 'user.is_anonymous() => True'


class GenericTest(TestCase):
    
    def test_plain(self):
        response = self.client.get('/generic/plain/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, PLAIN_RESPONSE)
    
    def test_context(self):
        response = self.client.get('/generic/context/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, CONTEXT_RESPONSE)
    
    def test_req_context(self):
        response = self.client.get('/generic/req_context/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, REQ_CONTEXT_RESPONSE)
