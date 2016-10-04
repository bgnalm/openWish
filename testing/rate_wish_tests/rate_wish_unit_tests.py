import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from open_wish_api import *
import unittest
import requests

VALID_RATING = 3
INVALID_RATING = 6

class RateWishTests(unittest.TestCase):

	def debug(self, s):
		debug_print('{0}: {1}'.format(self.id(), s))

	def test_rate_wish(self):
		user_name1 = 'test_rate_wish_creating_user{0}'.format(time.time())
		user_name2 = 'test_rate_wish_rating_user{0}'.format(time.time())

		self.debug('creating user {0}'.format(user_name1))
		response = create_new_user(user_name1)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('creating user {0}'.format(user_name2))
		response = create_new_user(user_name2)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('adding wish')
		response = add_wish(user_name1, 'wish text...', {'location':'Rehovot'})
		self.debug('received {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('reading wish')
		response = read_wish(user_name2)
		self.debug('received{0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('rating wish')
		response = rate_wish(user_name2, response['data']['wish_id'], VALID_RATING)
		self.debug('received {0}'.format(response))
		self.assertTrue(response['success'])


	def test_rate_unread_wish(self):
		user_name1 = 'test_rate_unread_wish_creating_user{0}'.format(time.time())
		user_name2 = 'test_rate_unread_wish_rating_user{0}'.format(time.time())

		self.debug('creating user {0}'.format(user_name1))
		response = create_new_user(user_name1)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('creating user {0}'.format(user_name2))
		response = create_new_user(user_name2)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('adding wish')
		response = add_wish(user_name1, 'wish text...', {'location':'Rehovot'})
		self.debug('received {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('rating wish')
		response = rate_wish(user_name2, response['data']['wish_id'], VALID_RATING)
		self.debug('received {0}'.format(response))
		self.assertFalse(response['success'])

	def test_rate_invalid_rating(self):
		user_name1 = 'test_rate_invalid_rating_creating_user{0}'.format(time.time())
		user_name2 = 'test_rate_invalid_rating_rating_user{0}'.format(time.time())

		self.debug('creating user {0}'.format(user_name1))
		response = create_new_user(user_name1)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('creating user {0}'.format(user_name2))
		response = create_new_user(user_name2)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('adding wish')
		response = add_wish(user_name1, 'wish text...', {'location':'Rehovot'})
		self.debug('received {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('reading wish')
		response = read_wish(user_name2)
		self.debug('received{0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('rating wish')
		response = rate_wish(user_name2, response['data']['wish_id'], INVALID_RATING)
		self.debug('received {0}'.format(response))
		self.assertFalse(response['success'])

	def test_rate_created_wish(self):
		user_name1 = 'test_rate_wish_creating_user{0}'.format(time.time())

		self.debug('creating user {0}'.format(user_name1))
		response = create_new_user(user_name1)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('adding wish')
		response = add_wish(user_name1, 'wish text...', {'location':'Rehovot'})
		self.debug('received {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('rating wish')
		response = rate_wish(user_name2, response['data']['wish_id'], VALID_RATING)
		self.debug('received {0}'.format(response))
		self.assertFalse(response['success'])

if __name__ == '__main__':
	unittest.main()
