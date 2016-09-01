import time

class Wish(object):

	def __init__(self, text, user_name, time_added=None, optional=None):
		self._text = text
		self._user_name = user_name
		self._time_added = time_added
		if time_added is None:
			self._time_added = int(time.time())

		self._optional = optional
		if type(optional) != dict and optional is not None:
			raise Exception('Optional has to be a dict')

class User(object):

	def __init__(self, name, created_wishes, read_wishes, posts, reads, last_post_timestamp, next_post_timestamp):
		self._name = name
		self._created_wishes = created_wishes
		self._read_wishes = read_wishes
		self._posts = posts
		self._reads = reads
		self._last_post_timestamp = last_post_timestamp
		self._next_post_timestamp = next_post_timestamp