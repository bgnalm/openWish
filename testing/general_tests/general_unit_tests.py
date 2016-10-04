from open_wish_api import *
import unittest
import requests

class GeneralTests(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(GeneralTests, self).__init__(*args, **kwargs)
		self._verbose = False
		for arg in sys.argv: 
			if arg == '-v':
				self._verbose = True

	def test_send_invalid_json(self):
		url = SERVER_ADDRESS + '/add_wish'
		if self._verbose:
			debug_print('test_send_invalid_json: sending invalid json request')

		r = request.post(url, data='asdbbbsdfg', headers=HEADERS)
		if self._verbose:
			debug_print('test_send_invalid_json: received \n'+str(r.json()))

		self.assertFalse(r.json()['success'])


