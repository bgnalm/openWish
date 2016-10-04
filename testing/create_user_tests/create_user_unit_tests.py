import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from open_wish_api import *
import unittest
import requests

class CreateUserTests(unittest.TestCase):

	def debug(self, s):
		debug_print('{0}: {1}'.format(self.id(), s))

	def test_create_user(self):
		user_name = 'test_create_user_{0}'.format(time.time())
		self.debug('creating user {0}'.format(user_name))
		response = create_new_user(user_name)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])

	def test_create_duplicate_users(self):
		user_name = 'test_create_duplicate_user_{0}'.format(time.time())
		self.debug('creating user {0}'.format(user_name))
		response = create_new_user(user_name)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])
		self.debug('creating duplicate user {0}'.format(user_name))
		response = create_new_user(user_name)
		self.debug('received {0}'.format(response))
		self.assertFalse(response['success'])

if __name__ == '__main__':
	unittest.main()
