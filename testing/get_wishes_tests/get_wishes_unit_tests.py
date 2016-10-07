import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from open_wish_api import *
import unittest
import requests

class GetWishesTests(unittest.TestCase):

	def debug(self, s):
		debug_print('{0}: {1}'.format(self.id(), s))

	def test_get_wishes(self):
		user_name1 = 'test_get_read_wishes_creating_user{0}'.format(time.time())
		user_name2 = 'test_get_read_wishes_getting_user{0}'.format(time.time())

		self.debug('creating user {0}'.format(user_name1))
		response = create_new_user(user_name1)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('creating user {0}'.format(user_name2))
		response = create_new_user(user_name2)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('getting wishes for user {0}'.format(user_name1))
		response = get_wishes(user_name1)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])
		self.assertTrue(len(response['data']['created_wishes'])==0)
		self.assertTrue(len(response['data']['read_wishes'])==0)

		self.debug('adding wish by user {0}'.format(user_name1))
		response = add_wish(user_name1, 'wish text...', {'location':'Rehovot'})
		self.debug('received {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('getting wishes for user {0}'.format(user_name1))
		response = get_wishes(user_name1)
		self.debug('received: {0}'.format(response))
		self.assertTrue(response['success'])
		self.assertTrue(len(response['data']['created_wishes'])==1)
		self.assertTrue(len(response['data']['read_wishes'])==0)

		self.debug('adding wish')
		response = add_wish(user_name2, 'wish text...', {'location':'Rehovot'})
		self.debug('received {0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('reading wish')
		response = read_wish(user_name1)
		self.debug('received{0}'.format(response))
		self.assertTrue(response['success'])

		self.debug('getting wishes for user {0}'.format(user_name1))
		response = get_wishes(user_name1)
		self.debug('received {0}'.format(response))
		self.assertTrue(response['success'])
		self.assertTrue(len(response['data']['created_wishes'])==1)
		self.assertTrue(len(response['data']['read_wishes'])==1)

if __name__ == '__main__':
	unittest.main()
