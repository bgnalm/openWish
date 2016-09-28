import traceback

REQUIRED_FIELDS = ['user_name', 'wish_id', 'rating']

def InvalidRatingError(Exception):
	pass

def UserDidNotReadWishError(Exception):
	pass

def main(db, request, consts):
	try:
		if request['rating'] > consts.MAXIMUM_RATING or request['rating'] < consts.MINIMUM_RATING:
			raise InvalidRatingError('Invalid rating: {0}'.format(request['rating']))

		db.user_rate_wish(
			request['user_name'],
			request['wish_id'],
			request['rating']
		)

		return {
			'success' : True,
			'message' : 'success'
		}



	except Exception, e:
		message = e.message
		if consts.FULL_TRACEBACK_MESSAGE:
			message = traceback.format_exc()
		return {
			'success' : False,
			'message' : message
		}
