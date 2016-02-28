import time

class Wish(object):

	def __init__(self, text, user_id, time_added=None, optional=None):
		self._text = text
		self._user_id = user_id
		self._time_added = time_added
		if time_added is None:
			self._time_added = int(time.time())

		self._optional = optional
		if type(optional) != dict and optional is not None:
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

	def get_random_wish(
		self,
		reader_user_id=None,
		add_to_read_wishes=None
	):
		"""
		@brief: returns a random wish
		@param reader_user_id: no wish by this user, or any wish that was already 
		@param add_to_read_wishes: should the retuned wish be added to the users
			read wishes list
		"""

		raise NotImplementedError('get_random_wish is not implemented')
