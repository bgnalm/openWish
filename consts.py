import time

LOCAL_SERVER = True

MINIMUM_RATING = 1
MAXIMUM_RATING = 5
USER_DIDNT_RATE_YET = -1

MINIMUM_MEXT_POST_TIME = 600 # 10 minutes
MAXIMUM_NEXT_POST_TIME = 3600 * 24 # 24 hours
ZERO_NEXT_POST_TIME = True # always allow to post, for debugging purposes

FULL_TRACEBACK_MESSAGE = True # should return full traceback in error messages

INITIAL_READS_LEFT = 3
NEW_WISH_READS_VALUE = 10 # how many reads does the user get from posting a new wish
RATE_WISH_READS_VALUE = 0.5 # how many reads does the user get from rating a wish

GET_WISHES_BATCH_SIZE = 10 # how many wishes are retrived for each get_wishes call

MONGODB_LOCAL_URI = '10.20.109.89'
MONGODB_MLAB_URL = 'mongodb://OpenWishAdmin:OpenWish@ds031193.mlab.com:31193/openwish'
DB_NAME = 'openwish'
MONGODB_URI = MONGODB_MLAB_URL
if LOCAL_SERVER:
	MONGODB_URI = MONGODB_LOCAL_URI
	DB_NAME = 'openWish'

class Wish(object):

	def __init__(self, text, user_name, wish_id='', read_by=[], number_of_reads=0,
		rating=0, number_of_ratings=0, disabled=False, time_added=None, optional=None):
		self._text = text
		self._wish_id = wish_id
		self._user_name = user_name
		self._time_added = time_added
		self._read_by = read_by
		self._number_of_reads = number_of_reads
		self._rating = rating
		self._number_of_ratings = number_of_ratings
		self._disabled = disabled
		if time_added is None:
			self._time_added = int(time.time())

		self._optional = optional
		if type(optional) != dict and optional is not None:
			raise Exception('Optional has to be a dict')

	def get_rating(self):
		if self._number_of_ratings == 0:
			return MINIMUM_RATING

		return self._rating / self._number_of_ratings

	def get_public_wish(self):
		return {
			'text' : self._text,
			'wish_id' : str(self._wish_id),
			'time_added' : self._time_added,
			'rating' : self.get_rating(),
			'number_of_reads' : self._number_of_reads,
			'optional' : self._optional
		}

class User(object):

	def __init__(self, name, created_wishes, read_wishes, last_read_wish, reads_left, posts, reads, last_post_timestamp, next_post_timestamp):
		self._name = name
		self._created_wishes = created_wishes
		self._read_wishes = read_wishes
		self._last_read_wish = last_read_wish
		self._reads_left = reads_left
		self._posts = posts
		self._reads = reads
		self._last_post_timestamp = last_post_timestamp
		self._next_post_timestamp = next_post_timestamp
		