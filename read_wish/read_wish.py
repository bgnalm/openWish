import traceback

REQUIRED_FIELDS = ['user_name']

def main(db, request, consts):
	try:
		wish = db.get_random_wish(reader_user_name=request['user_name'], add_to_read_wishes=True)
		return {
			'success' : True,
			'data' : wish.get_public_wish()
		}

	except Exception, e:
		message = e.message
		if consts.FULL_TRACEBACK_MESSAGE:
			message = traceback.format_exc()
		return {
			'success' : False,
			'message' : message
		}
		