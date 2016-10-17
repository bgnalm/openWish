import time

MINIMUM_RATING = 1
MAXIMUM_RATING = 5
USER_DIDNT_RATE_YET = -1

MINIMUM_MEXT_POST_TIME = 600 # 10 minutes
MAXIMUM_NEXT_POST_TIME = 3600 * 24 # 24 hours
ZERO_NEXT_POST_TIME = True # always allow to post, for debugging purposes

FULL_TRACEBACK_MESSAGE = True # should return full traceback in error messages


class Wish(object):

	def __init__(self, text, user_name, wish_id='', read_by=[], number_of_reads=0,
		rating=0, number_of_ratings=0, time_added=None, optional=None):
		self._text = text
		self._wish_id = wish_id
		self._user_name = user_name
		self._time_added = time_added
		self._read_by = read_by
		self._number_of_reads = number_of_reads
		self._rating = rating
		self._number_of_ratings = number_of_ratings
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

	def __init__(self, name, created_wishes, read_wishes, posts, reads, last_post_timestamp, next_post_timestamp):
		self._name = name
		self._created_wishes = created_wishes
		self._read_wishes = read_wishes
		self._posts = posts
		self._reads = reads
		self._last_post_timestamp = last_post_timestamp
		self._next_post_timestamp = next_post_timestamp