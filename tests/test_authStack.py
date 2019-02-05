from unittest import TestCase

from connector.auth_stack import AuthStack


class TestAuthStack(TestCase):
    def test_pop(self):
        single_auth = AuthStack()
        single_auth.pop()
        second_single_auth = AuthStack()
        self.assertTrue(second_single_auth.is_empty())
