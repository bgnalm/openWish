import traceback

REQUIRED_FIELDS = ['user_name', 'wish_id']

def WishNotFoundError(Exception):
	def __init__(self, wish_id):
		super(WishNotFoundError, self).__init__('wish {0} was not found'.format(wish_id))

def main(db, request, consts):
	try:
		user = db.load_user(request['user_name'])
		wish_found = False
		for wish in user._created_wishes:
			if str(wish) == request['wish_id']:
				wish_found = True
				break

		if not wish_found:
			for wish in user._created_wishes:
				if str(wish['wish_id']) == request['wish_id']:
					wish_found = True
					break

		if not wish_found:
			raise WishNotFoundError(request['wish_id'])

		wish = db.load_wish(request['wish_id'])
		return {
			'success' : True,
			'data' : {
				'text' : wish._text,
				'time_added' : wish._time_added,
				'user_name' : wish._user_name,
				'rating' : wish.get_rating(),
				'number_of_reads' : wish._number_of_reads,
				'optional': wish._optional
			}
		}

	except Exception, e:
		message = e.message
		if consts.FULL_TRACEBACK_MESSAGE:
			message = traceback.format_exc()
		return {
			'success' : False,
			'message' : message
		}