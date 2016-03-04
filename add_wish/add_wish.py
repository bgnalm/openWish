import json


def main(db, data, consts):
	json_request = None
	try:
		json_request = json.loads(data)

	except ValueError:
		return consts.REQUEST_JSON_PARSING_ERROR

