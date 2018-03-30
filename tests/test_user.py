"""Test case for the user"""
import json
from tests.test_base import BaseTestCase


class AuthTestCase(BaseTestCase):
    """Test case for the user"""
    def test_registration(self):
        """Test user registration works correcty."""
        res = self.register_user()
        self.assertTrue(res.content_type == 'application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Account created successfully")
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        self.register_user()
        second_res = self.register_user()
        self.assertTrue(second_res.content_type == 'application/json')
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "User already exists")
        self.assertEqual(second_res.status_code, 409)

    def test_user_login(self):
        """Test registered user can login."""
        self.register_user()
        res = self.login_user()
        self.assertTrue(res.content_type == 'application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Login successfull")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(result['access_token'])
