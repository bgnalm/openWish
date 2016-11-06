import DB
from pymongo import MongoClient
from bson.objectid import ObjectId
import time
import consts
import random

MONGO_URI = '10.20.109.89'
MONGO_MLAB = 'mongodb://OpenWishAdmin:OpenWish@ds031193.mlab.com:31193/openwish'
DB_NAME = 'openwish'

class UserExistsError(Exception):
	pass

class UserDoesNotExistsError(Exception):
	pass

class UserCantRateWish(Exception):
	pass

class UserCantStarWish(Exception):
	pass

class MongoInterface(DB.DBInterface):

	def _add_created_wish_to_user(self, user_name, wish_id):
		self._users.update(
			{'name':user_name},
			{'$push': {'created_wishes':wish_id}, '$inc' : {'posts' : 1}}
		)

	def _map(self, value, start1, stop1, start2, stop2):
		distance = value - start1
		part = distance / float(stop1 - start1)
		return (stop2 - start2) * part + start2

	def _map_rating_to_next_post(self, average_rating):
		r = consts.MAXIMUM_RATING - average_rating
		time_to_wait = self._map(
			average_rating, 
			consts.MINIMUM_RATING, 
			consts.MAXIMUM_RATING, 
			consts.MINIIMUM_NEXT_POST_TIME,
			consts.MAXIMUM_NEXT_POST_TIME
		)

		return time.time() + time_to_wait

	def _calculate_user_next_post_time(self, user_name):
		if consts.ZERO_NEXT_POST_TIME:
			return 0

		created_wishes = self._users.find({'name':user_name}).limit(1).next()['created_wishes']
		total_ratings = 0
		total_number_of_ratings = 0
		for wish_id in created_wishes:
			current_wish = self._wishes.find({'_id':wish_id}).limit(1).next()
			total_ratings += current_wish['rating']
			total_number_of_ratings+= current_wish['number_of_ratings']

		if total_number_of_ratings == 0:
			return time.time() + consts.MAXIMUM_NEXT_POST_TIME
		else:
			total_average = total_ratings/float(total_number_of_ratings)
			return self._map_rating_to_next_post(total_average)

	def _update_user_post_data(self, user_name, post_time):
		next_post_time = self._calculate_user_next_post_time(user_name)
		self._users.update(
			{'name' : user_name},
			{
				'$set' : {
					'last_post_timestamp' : post_time,
					'next_post_timestamp' : int(next_post_time)
				}
			}
		)

	def _update_user_after_new_wish(self, user_name, wish_id, post_time):
		next_post_time = self._calculate_user_next_post_time(user_name)
		self._users.update(
			{'name':user_name},
			{
				'$push': {'created_wishes':wish_id}, '$inc' : {'posts' : 1},
				'$set' : {
					'last_post_timestamp' : post_time,
					'next_post_timestamp' : int(next_post_time)
				},
				'$inc' : {'reads_left' : consts.NEW_WISH_READS_VALUE}
			}
		)

	def _add_read_wish_to_user(self, user_name, wish_id):
		self._users.update(
			{'name':user_name},
			{
				'$push': {
					'read_wishes':
							{
								'wish_id':wish_id, 
								'rating':consts.USER_DIDNT_RATE_YET, 
								'starred' : False
							}
				},
				'$inc' : {'reads' : 1}	
			},
		)

		self._wishes.update(
			{'_id' : wish_id},
			{'$push' : {'read_by' : user_name}}
		)

	def _user_exists(self, name):
		result = self._users.find({'name':name}).limit(1)
		if result.count() >= 1:
			return True

		return False

	def _get_wishes_data(self, wishes):
		"""
		@brief: gets a list of wishes
		"""

		data = []
		result = self._wishes.find(
			{'_id': {'$in' : wishes}}
		)

		for wish in result:
			w = consts.Wish(
				wish['text'],
				wish['user_name'],
				wish['_id'],
				None,
				wish['number_of_reads'],
				wish['rating'],
				wish['number_of_ratings'],
				wish['disabled'],
				wish['time_added'],
				wish['optional']
			)
			data.append(w.get_public_wish())

		return data

	def __init__(self):
		#self._db = MongoClient(MONGO_URI)[DB_NAME]
		self._db = MongoClient(consts.MONGODB_URI)[consts.DB_NAME]
		self._wishes = self._db['wishes']
		self._users = self._db['users']
		self._bugs = self._db['bugs']

	def load_user(self, user_name):
		if not self._user_exists(user_name):
			raise UserDoesNotExistsError('User {0} does not exist'.format(user_name))

		result = self._users.find({'name':user_name}).limit(1).next()
		return consts.User(
			user_name,
			result['created_wishes'],
			result['read_wishes'],
			result['last_read_wish'],
			result['reads_left'],
			result['posts'],
			result['reads'],
			result['last_post_timestamp'],
			result['next_post_timestamp']
		)

	def load_wish(self, wish_id):
		"""
		wish_id: if you have the id of the wish
		wish: if you have the result of a find
		"""

		result = self._wishes.find({'_id': ObjectId(wish_id)}).limit(1).next()

		return consts.Wish(
			result['text'],
			result['user_name'],
			wish_id,
			result['read_by'],
			result['number_of_reads'],
			result['rating'],
			result['number_of_ratings'],
			result['disabled'],
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
			'last_read_wish' : None,
			'reads_left' : consts.INITIAL_READS_LEFT,
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
			'number_of_ratings' : 0,
			'disabled' : False
		}

		if not self._user_exists(wish._user_name):
			raise UserDoesNotExistsError('User {0} does not exists'.format(wish._user_name))

		_id = self._wishes.insert(insertion)
		self._update_user_after_new_wish(wish._user_name, _id, wish._time_added)
		return _id

	def get_random_wish(
		self,
		reader_user_name,
		add_to_read_wishes
	):
		"""
		@note: this is not the best implmentation
			the best implemantation is to add a randon 0 to 1 field to each
			wish, and search for when some random is bigger than the random field
			the current implemantation just returns the first possible value
		"""

		read_wishes = self._users.find({'name':reader_user_name}).limit(1).next()['read_wishes']
		read_wishes_id = [wish['wish_id'] for wish in read_wishes]
		created_wishes = self._users.find({'name':reader_user_name}).limit(1).next()['created_wishes']
		excluded_wishes = read_wishes_id + created_wishes
		excluded_wishes_id = [ObjectId(wish) for wish in excluded_wishes]
		wishes = self._wishes.find({'_id':{'$nin':excluded_wishes_id}})
		wish_number = random.randint(0, wishes.count()-1)
		wishes.skip(wish_number)
		wish = wishes.next()
		if add_to_read_wishes:
			self._add_read_wish_to_user(reader_user_name, ObjectId(wish['_id']))

		return self.load_wish(wish['_id'])

	def user_rate_wish(self, user_name, wish_id, rating):
		wish_object = ObjectId(wish_id)
		result = self._users.find({
			'$and' : [
				{'name' : user_name},
				{'read_wishes' : {'$elemMatch' :{'wish_id':wish_object}}}
			]
		})

		if result.count() == 0:
			raise UserCantRateWish('user {0} cant rate wish {1]'.format(user_name, wish_id))

		initial_rating = 0
		for read_wish in result.next()['read_wishes']:
			if read_wish['wish_id'] == wish_object:
				initial_rating = read_wish['rating']

		self._users.update(
			{'name' : user_name, 'read_wishes.wish_id': wish_object}, 
			{
				'$set' : {'read_wishes.$.rating' : rating},
				'$inc' : {'reads_left' : consts.RATE_WISH_READS_VALUE}
			}
		)

		if initial_rating == consts.USER_DIDNT_RATE_YET:
			self._wishes.update(
				{'_id' : wish_object},
				{
				 '$inc' : {'rating' : rating, 'number_of_ratings' : 1},	
				}
			)

		else:
			self._wishes.update(
				{'_id' : wish_object},
				{
				 '$inc' : {'rating' : rating-initial_rating},	
				}
			)

	def star_wish(self, user_name, wish_id, starred):
		wish_object = ObjectId(wish_id)
		result = self._users.update(
			{'name' : user_name, 'read_wishes.wish_id': wish_object}, 
			{
				'$set' : {'read_wishes.$.starred' : starred},
			}
		)

		if result.items()[0][1] == 0:
			raise UserCantStarWish('user {0} has not read wish {1}'.format(user_name,wish_id))

	def get_batch_wishes(self, username, counter, read_wishes, created_wishes, starred_wishes):
		if not self._user_exists(username):
			raise UserDoesNotExistsError('User {0} does not exist'.format(username))

		read_wishes_batch_size = 1
		created_wishes_batch_size = 1
		starred_wishes_batch_size = 1
		if read_wishes:
			read_wishes_batch_size = consts.GET_WISHES_BATCH_SIZE
		if created_wishes:
			created_wishes_batch_size = consts.GET_WISHES_BATCH_SIZE
		if starred_wishes:
			starred_wishes_batch_size = consts.GET_WISHES_BATCH_SIZE

		read_wishes_data = []
		created_wishes_data = []
		starred_wishes_data = []

		if read_wishes:
			result = self._users.find(
				{'name' : username},
				{
					'read_wishes' : {'$slice' : [counter, read_wishes_batch_size]},
					'created_wishes' : 0,
				}
			).next()

			read_wishes_id = [wish['wish_id'] for wish in result['read_wishes']]
			read_wishes_data = self._get_wishes_data(read_wishes_id)

		if created_wishes:
			result = self._users.find(
				{'name' : username},
				{
					'read_wishes' : 0,
					'created_wishes' : {'$slice' : [counter, created_wishes_batch_size]},
				}
			).next()

			created_wishes_data = self._get_wishes_data(result['created_wishes'])

		if starred_wishes:
			result = self._users.find(
				{'name' : username},
				{
					'read_wishes' : 1,
				}
			).next()

			starred_wishes_id = []
			for wish in result['read_wishes']:
				if wish['starred']:
					starred_wishes_id.append(wish['wish_id'])

			starred_wishes_data = self._get_wishes_data(starred_wishes_id)

		return {
			'read_wishes': read_wishes_data,
			'created_wishes' : created_wishes_data,
			'starred_wishes' : starred_wishes_data
		}

	def add_bug(self, bug, username, time_added):
		insertion = {
			'text' : bug,
			'time_added' : time_added,
			'user_name' : username
		}

		self._bugs.insert(insertion)





		
