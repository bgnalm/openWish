import json
import requests
import time
import sys

SERVER_ADDRESS = 'http://127.0.0.1:5000'
HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

VERBOSE = False
LOG_FILE = 'unit_test_log.txt'

def create_new_user(username):
	"""
	@return: true/false is worked
	"""
	url = SERVER_ADDRESS + '/create_user'
	data = {
		'user_name' : username
	}

	r = requests.post(url, data=json.dumps(data), headers=HEADERS)
	return r.json()

def add_wish(username, text, optional):
	url = SERVER_ADDRESS + '/add_wish'
	data = {
		'user_name' : username,
		'wish' : {
			'text' : text,
			'optional' : optional
		}
	}

	r = requests.post(url, data=json.dumps(data), headers=HEADERS)
	return r.json()

def rate_wish(user_name, wish_id, rating):
	url = SERVER_ADDRESS + '/rate_wish'
	data = {
		'user_name' : user_name,
		'wish_id' : wish_id,
		'rating' : rating
	}

	r = requests.post(url, data=json.dumps(data), headers=HEADERS)
	return r.json()

def read_wish(username):
	url = SERVER_ADDRESS + '/read_wish'
	data = {
		'user_name' : username
	}

	r = requests.post(url, data=json.dumps(data), headers=HEADERS)
	return r.json()

def get_wishes(username):
	url = SERVER_ADDRESS + '/get_wishes'
	data = {
		'user_name' : username
	}

	r = requests.post(url, data=json.dumps(data), headers=HEADERS)
	return r.json()

def get_wish(username, wish_id):
	url = SERVER_ADDRESS + '/get_wish'
	data = {
		'user_name' : username,
		'wish_id' : wish_id
	}

	r = requests.post(url, data=json.dumps(data), headers=HEADERS)
	return r.json()

def star_wish(username, wish_id, star_wish):
	url = SERVER_ADDRESS + '/star_wish'
	data = {
		'user_name' : username,
		'wish_id' : wish_id,
		'starred' : star_wish
	}

	r = requests.post(url, data=json.dumps(data), headers=HEADERS)
	return r.json()

def get_permissions(username):
	url = SERVER_ADDRESS + '/get_permissions'
	data = {
		'user_name' : username,
	}

	r = requests.post(url, data=json.dumps(data), headers=HEADERS)
	return r.json()

def get_btach_wishes(username, read_wishes, created_wishes, starred_wihes, counter):
	url = SERVER_ADDRESS + '/get_wishes_extended'
	data = {
		'user_name' : username,
		'counter' : counter,
		'read_wishes' : read_wishes,
		'created_wishes' : created_wishes,
		'starred_wishes' : starred_wishes
	}

	r = requests.post(url, data=json.dumps(data), headers=HEADERS)
	return r.json()


def debug_print(s):
	message = time.ctime() + ': ' + s
	if VERBOSE:
		print message
	
	f = open(LOG_FILE, 'a')
	f.write(message+'\n')
	f.close()






