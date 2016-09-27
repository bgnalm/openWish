import traceback

REQUIRED_FIELDS = ['user_name']

def get_created_wishes_id(user):
	return [str(wish) for wish in user._created_wishes]

def get_read_wishes_id(user):
	return [str(wish['wish_id']) for wish in user._read_wishes]

def main(db, request, consts):
	try:
		response = {
			'success' : True,
			'data' : {}
		}

		user = db.load_user(request['user_name'])
		
		request_specified_data = False
		if 'created_wishes' in request.keys() and request['created_wishes']:
			request_specified_data = True
			response['data']['created_wishes'] = get_created_wishes_id(user)

		if 'read_wishes' in request.keys() and request['read_wishes']:
			request_specified_data = True
			response['data']['read_wishes'] = get_read_wishes_id(user)

		if not request_specified_data:
			response['data']['created_wishes'] = get_created_wishes_id(user)
			response['data']['read_wishes'] = get_read_wishes_id(user)

		return response

	except Exception, e:
		message = e.message
		if consts.FULL_TRACEBACK_MESSAGE:
			message = traceback.format_exc()
		return {
			'success' : False,
			'message' : message
		}
