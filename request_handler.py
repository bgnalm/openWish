import json

class JsonRequestParsingError(Exception):
	pass

class NoRequiredFieldError(Exception):
	
	def __init__(self, message, missing_field):
		super(NoRequiredFieldError, self).__init__(message)
		self._field = missing_field

def handle_json_request(data, required_fields=None):
	try:
		json_request = json.loads(data)

	except ValueError:
		raise JsonRequestParsingError	

	if required_fields == None:
		return json_request

	for key in required_fields:
		if not json_request.has_key(key):
			raise NoRequiredFieldError('cant find field "{0}"'.format(key), key)

	return json_request

DEFAULT_REQUIRED_FIELDS = [
	'success',
	'message',
]

def handle_response(response, required_fields=DEFAULT_REQUIRED_FIELDS):
	new_response = response
	if 'message' not in new_response.keys() and new_response['success'] == True:
		new_response['message'] = 'success'

	for required_field in required_fields:
		if required_field not in new_response.keys():
			raise NoRequiredFieldError('no {0} in response {1}'.format(required_field, new_response), required_field)

	return json.dumps(new_response)

