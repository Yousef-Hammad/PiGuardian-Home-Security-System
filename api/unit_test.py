import sys
import os
import unittest
from unittest.mock import patch
from api.controller import add_user, login
user_name = 'Hamdiata Diakite'
user_username = 'hamdiatadiakite'
user_email = 'diakitehamdiata'
user_number = '819-213-6364'
pwd = 'SYSC3010'


class TestController(unittest.TestCase):
    def setUp(self):
        # Setup that runs before each test method
       
        self.valid_user_info = {
            'name': user_name,
            'username': user_username,
            'email': user_email,
            'phone_number': user_number,
            'password': pwd
        }

   

    @patch('controller.get_user_from_firestore')
    @patch('controller.get_user_attribute')
    def test_login_success(self, mock_get_user_attribute, mock_get_user_from_firestore):
        # Simulate database response for existing user
        mock_get_user_from_firestore.return_value = self.valid_user_info
        # Simulate retrieving the user's password attribute
        mock_get_user_attribute.return_value = self.valid_user_info['password']

        # Attempt to login with correct credentials
        result = login(self.valid_user_info['username'], self.valid_user_info['password'])

        # Assert login was successful
        self.assertTrue(result)

        print("Login passed")
        
    @patch('controller.get_user_from_firestore')
    def test_login_failure_user_not_found(self, mock_get_user_from_firestore):
        # Simulate user not found in the database
        mock_get_user_from_firestore.return_value = None

        # Attempt to login with a username that doesn't exist
        result = login('Bisher', 'SYSC3010')

        # Assert login failed
        self.assertFalse(result)
        print("User not found passed")
        
    @patch('controller.get_user_from_firestore')
    @patch('controller.get_user_attribute')
    def test_login_failure_wrong_password(self, mock_get_user_attribute, mock_get_user_from_firestore):
        # Simulate database response for existing user
        mock_get_user_from_firestore.return_value = self.valid_user_info
        # Simulate retrieving the user's password attribute, but provide a wrong password
        mock_get_user_attribute.return_value = 'SYSC'

        # Attempt to login with correct username but wrong password
        result = login(self.valid_user_info['username'], 'wrongPassword')

        # Assert login failed
        self.assertFalse(result)
        print("wrong password check passed")
        
# This enables running the tests from the command line
if __name__ == '__main__':
    unittest.main()
