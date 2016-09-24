import traceback

REQUIRED_FIELDS = ['user_name']

def main(db, requests, consts):
	try:
		wish = db.get_random_wish(reader_user_name=request['user_name'], add_to_read_wishes=True)
		return {
			'success' : True,
			'data' : {
				'text' : wish.text,
				'time_added' : wish.time_added,
				'user_name' : wish.user_name,
				'rating' : wish.rating,
				'number_of_reads' : wish.number_of_reads,
				'optinal' : wish.optional
			}
		}

	except Exception, e:
		return {
			'success' : False,
			'message' : traceback.format_exc()
		}
		