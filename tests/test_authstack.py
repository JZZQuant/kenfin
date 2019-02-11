import time
from unittest import TestCase

from connector.auth_stack import AuthSingletonStack


class AuthStackTests(TestCase):
    def test_pop(self):
        single_auth = AuthSingletonStack()
        single_auth.pop()
        second_single_auth = AuthSingletonStack()
        self.assertTrue(second_single_auth.is_empty())

    def test_del(self):
        single_auth = AuthSingletonStack()
        single_auth.pop()
        del single_auth
        second_single_auth = AuthSingletonStack()
        self.assertFalse(second_single_auth.is_empty())
