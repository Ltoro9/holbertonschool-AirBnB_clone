#!/usr/bin/python3
'''
    test_user.py
    
    Unittest for class city
'''
import unittest
from models.user import User
from models.base_model import BaseModel


class test_user(unittest.TestCase):
    '''
        Class User Unittest
    '''

    def test_user(self):
        '''
            Class User test cases
        '''

        # Check if user has the expected attrs
        user = User()
        self.assertTrue(hasattr(user, 'email'))
        self.assertTrue(hasattr(user, 'password'))
        self.assertTrue(hasattr(user, 'first_name'))
        self.assertTrue(hasattr(user, 'last_name'))

        # Check if attrs are initialized to empty strs
        self.assertEqual(user.email, '')
        self.assertEqual(user.password, '')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')

    def test_inheritance(self):
        '''
            Check if class inherits from BaseModel
        '''
        user = User()

        # Check if User class inherits from BaseModel
        self.assertTrue(issubclass(User, BaseModel))


if __name__ == '__main__':
    unittest.main()
