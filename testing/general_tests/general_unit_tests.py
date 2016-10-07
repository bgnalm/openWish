import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from open_wish_api import *
import unittest
import requests
import json

class GeneralTests(unittest.TestCase):

	def debug(self, s):
		debug_print('{0}: {1}'.format(self.id(), s))

	def test_send_invalid_json(self):
		url = SERVER_ADDRESS + '/add_wish'
		self.debug('test_send_invalid_json: sending invalid json request')
		r = requests.post(url, data='asdbbbsdfg', headers=HEADERS)
		self.debug('test_send_invalid_json: received \n'+str(r.raw.read(10)))
		self.assertFalse(r.json()['success'])

	def test_send_request_without_requierd_field(self):
		url = SERVER_ADDRESS + '/add_wish'
		self.debug('test_send_request_without_requierd_field')
		request = {
			'wish'  : {
				'text' : 'lolololo i hope this fails',
				'optional' : {
					'metadata' : 'so meta'
				}
			}
		}
		r = requests.post(url, data=json.dumps(request), headers=HEADERS)
		self.debug('test_send_request_without_requierd_field')

if __name__ == '__main__':
	unittest.main()


