import DB
from pymongo import MongoClient
import time
import consts

MONGO_URI = '10.20.109.89'
DB_NAME = 'openWish'

class UserExistsError(Exception):
	pass

class UserDoesNotExistsError(Exception):
	pass

class MongoInterface(DB.DBInterface):

	def _get_all_created_wishes(self, user_id):
		return self._users.find({'_id':user_id}).created_wishes

	def _get_all_read_wishes(self, user_id):
		return self._users.find({'_id':user_id}).read_wishes

	def _add_created_wish_to_user(self, user_name, wish_id):
		self._users.update(
			{'name':user_name},
			{'$push': {'created_wishes':wish_id}, '$inc' : {'posts' : 1}}
		)

	def _add_read_wish_to_user(self, user_name, wish_id, rating=None):
		user_rating = 0
		if rating is not None and type(rating) == int:
			user_rating = rating

		self._users.update(
			{'name':user_name},
			{'$push': {'read_wishes':{'wish_id':wish_id, 'rating':user_rating}}},
		)

	def _user_exists(self, name):
		result = self._users.find({'name':name}).limit(1)
		if result.count() >= 1:
			return True

		return False


	def __init__(self):
		self._db = MongoClient(MONGO_URI)[DB_NAME]
		self._wishes = self._db['wishes']
		self._users = self._db['users']

	def load_user(self, user_name, user=None):
		if not self._user_exists(user_name):
			raise UserDoesNotExistsError('User {0} does not exist'.format(user_name))

		result = self._users.find({'name':user_name}).limit(1).next()
		return consts.User(
			user_name,
			result['created_wishes'],
			result['read_wishes'],
			result['posts'],
			result['reads'],
			result['last_post_timestamp'],
			result['next_post_timestamp']
		)

	def load_wish(self, wish_id, wish=None):
		"""
		wish_id: if you have the id of the wish
		wish: if you have the result of a find
		"""
		if wish is None:
			result = self._wishes.find({'_id':wish_id}).limit(1).next()
		else:
			result = wish

		return consts.Wish(
			result['text'],
			result['user_name'],
			result['read_by'],
			result['number_of_reads'],
			result['rating'],
			result['number_of_ratings']
			result['time_added'],
			result['optional'],

		)

	def next_read(self, name):
		if not self._user_exists(name):
			raise UserDoesNotExistsError('User {0} does not exist'.format(name))

		result = self._users.find({'name':name}).limit(1).next()
		return result['next_read_timestamp']

	def create_user(self, name):
		if self._user_exists(name):
			raise UserExistsError('User {0} already exists'.format(name))

		insertion = {
			'name' : name,
			'created_wishes' : [],
			'read_wishes' : [],
			'last_post_timestamp' : 0,
			'next_post_timestamp' : 0,
			'posts' : 0,
			'reads' : 0
		}

		_id = self._users.insert(insertion)
		return _id


	def insert_wish(self, wish):
		insertion = {
			'time_added':wish._time_added, 
			'text':wish._text, 
			'user_name' :wish._user_name,
			'optional': wish._optional,
			'read_by' : [],
			'number_of_reads' : 0,
			'rating' : 0,
			'number_of_ratings' : 0
		}

		if not self._user_exists(wish._user_name):
			raise UserDoesNotExistsError('User {0} does not exists'.format(wish._user_name))

		_id = self._wishes.insert(insertion)
		self._add_created_wish_to_user(wish._user_name, str(_id))
		return _id

	def get_random_wish(
		self,
		reader_user_name=None,
		add_to_read_wishes=None
	):
		"""
		@note: this is not the best implmentation
			the best implemantation is to add a randon 0 to 1 field to each
			wish, and search for when some random is bigger than the random field
			the current implemantation just returns the first possible value
		"""

		read_wishes = self._get_all_read_wishes()
		created_wishes = self._get_all_created_wishes()
		excluded_wishes = read_wishes + created_wishes
		wish = self._wishes.find({'_id':{'$nin':excluded_wishes}}).limit(1)
		if type(add_to_read_wishes) == bool and add_to_read_wishes:
			self._add_read_wish_to_user(reader_user_name, wish._id)

		return self.load_wish(wish)




		
