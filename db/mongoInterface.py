import DB
from pymongo import MongoClient
import time

MONGO_URI = '10.20.109.89'
DB_NAME = 'openWish'

class MongoInterface(DB.DBInterface):

	def _get_all_created_wishes(self, user_id):
		return self._users.find({'_id':user_id}).created_wishes

	def _get_all_read_wishes(self, user_id):
		return self._users.find({'_id':user_id}).read_wishes

	def _add_created_wish_to_user(self, user_id, wish_id):
		self._users.update(
			{'_id':user_id},
			{'$push': {'created_wishes':{'wish_id':wish_id}}}
		)

	def _add_read_wish_to_user(self, user_id, wish_id, rating=None):
		user_rating = 0
		if rating is not None and type(rating) == int:
			user_rating = rating

		self._users.update(
			{'_id':user_id},
			{'$push': {'read_wishes':{'wish_id':wish_id, 'rating':user_rating}}}
		)

	def __init__(self):
		self._db = MongoClient(MONGO_URI)[DB_NAME]
		self._wishes = self._db['wishes']
		self._users = self._db['users']

	def create_user(self, name):
		insertion = {
			'name' : name,
			'created_wishes' : [],
			'read_wishes' : [],
			'last_read_timestamp ' : 0
		}

		_id = self._users.insert(insertion)
		return _id


	def insert_wish(self, wish):
		insertion = {
			'time_added':wish._time_added, 
			'text':wish._text, 
			'user_id':wish._user_id,
			'optional': wish._optional
		}

		_id = self._wishes.insert(insertion)
		self._add_created_wish_to_user(wish._user_id, str(_id))
		return _id

	def get_random_wish(
		self,
		reader_user_id=None,
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
			self._add_read_wish_to_user(reader_user_id, wish._id)

		return wish




		
