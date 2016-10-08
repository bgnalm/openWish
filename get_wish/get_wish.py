import traceback

REQUIRED_FIELDS = ['user_name', 'wish_id']

class WishNotFoundError(Exception):
	pass

def main(db, request, consts):
	try:
		user = db.load_user(request['user_name'])
		wish_found = False
		for wish in user._created_wishes:
			if str(wish) == request['wish_id']:
				wish_found = True
				break

		if not wish_found:
			for wish in user._read_wishes:
				if str(wish['wish_id']) == request['wish_id']:
					wish_found = True
					break

		if not wish_found:
			raise WishNotFoundError('wish {0} was not found'.format(request['wish_id']))

		wish = db.load_wish(request['wish_id'])
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