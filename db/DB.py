import time

class Wish(object):

	def __init__(self, text, user_id, date_added=None, optional=None):
		self._text = text
		self._user_id = user_id
		self._date_added = date_added
		if date_added is None:
			self._date_added = int(time.time())

		self._optional = optional
		if type(optional) != dict:
			raise Exception('Optional has to be a dict')
		

class DBInterface(object):
	"""
	@brief: An interface class that incapsulates all operations that db modules should support
	"""

	def insert_wish(self, wish):
		"""
		@brief: adds a new wish
		"""

		raise NotImplementedError('Insert wish is not implemented')

	def get_random_wish(self, user_id_to_exclude=None):
		"""
		@brief: returns a random wish
		@param user_id_to_exclude: don't return wishes from this user
		"""

		raise NotImplementedError('get_random_wish is not implemented')
