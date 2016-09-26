import json
import requests
import time
import termcolor
import unittest
import sys

SERVER_ADDRESS = 'http://127.0.0.1:5000'
HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

class TestBasicCases(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestBasicCases, self).__init__(*args, **kwargs)
		self._verbose = False
		for arg in sys.argv: # not pretty
			if arg == '-v':
				self._verbose = True

	def generate_user_name(self):
		return time.ctime().replace(' ', '_')

	def create_new_user(self, username):
		"""
		@return: true/false is worked
		"""
		url = SERVER_ADDRESS + '/create_user'
		data = {
			'user_name' : username
		}

		if self._verbose:
			print 'create_new_user: sending\n' + str(data)

		r = requests.post(url, data=json.dumps(data), headers=HEADERS)

		if self._verbose:
			print 'create_new_user: got\n' + str(r.json())

		return r.json()['success']

	def add_wish(self, username, text, optional):
		url = SERVER_ADDRESS + '/add_wish'
		data = {
			'user_name' : username,
			'wish' : {
				'text' : text,
				'optional' : optional
			}
		}

		if self._verbose:
			print 'add_wish: sending\n' + str(data)

		r = requests.post(url, data=json.dumps(data), headers=HEADERS)

		if self._verbose:
			print 'add_wish: got\n' + str(r.json())

		return r.json()['success']

	def read_wish(self, username):
		url = SERVER_ADDRESS + '/read_wish'
		data = {
			'user_name' : username
		}

		if self._verbose:
			print 'read_wish: sending\n' + str(data)

		r = requests.post(url, data=json.dumps(data), headers=HEADERS)

		if self._verbose:
			print 'read_wish: got\n' + str(r.json())

		return r.json()['success']

	def test_same_user_twice(self):
		"""
		tests that if someone tries to register with an already existing user is denied
		"""
		
		user_name = 'same_user_test_'+self.generate_user_name()
		self.assertTrue(self.create_new_user(user_name))
		self.assertFalse(self.create_new_user(user_name))

	def test_create_and_post(self):
		user_name = 'test_create_and_post_'+self.generate_user_name()
		self.assertTrue(self.create_new_user(user_name))
		self.assertTrue(self.add_wish(user_name, 'i wish this test will pass', {'metadata': 'really meta'}))

	def test_add_and_read_wish(self):
		user_name1 = 'test_add_and_read_wish1'+self.generate_user_name()
		user_name2 = 'test_add_and_read_wish2'+self.generate_user_name()
		self.create_new_user(user_name1)
		self.create_new_user(user_name2)
		self.assertTrue(self.add_wish(user_name1, 'i wish this test will pass', {'metadata': 'really meta'}))
		self.assertTrue(self.read_wish(user_name2))

if __name__ == '__main__':
	unittest.main()




