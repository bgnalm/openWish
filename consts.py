
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

REQUEST_JSON_PARSING_ERROR = "The sent request isn't in json format"