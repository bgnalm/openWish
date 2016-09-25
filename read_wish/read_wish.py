import traceback

REQUIRED_FIELDS = ['user_name']

def main(db, request, consts):
	try:
		wish = db.get_random_wish(reader_user_name=request['user_name'], add_to_read_wishes=True)
		return {
			'success' : True,
			'data' : {
				'text' : wish.text,
				'time_added' : wish.time_added,
				'user_name' : wish.user_name,
				'rating' : wish.rating/float(wish.number_of_ratings),
				'number_of_reads' : wish.number_of_reads,
				'optinal' : wish.optional
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
		