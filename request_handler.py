import json

class JsonRequestParsingError(Exception):
	pass

class NoRequiredFieldError(Exception):
	pass

def handle_json_request(data, required_fields=None):
	try:
		json_request = json.loads(data)

	except ValueError:
		raise JsonRequestParsingError

	if required_fields == None:
		return json_request

	for key in required_fields:
		if not json_request.has_key(key):
			raise NoRequiredFieldError

	return json_request

	

