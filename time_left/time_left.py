import time

REQUIRED_FIELDS = ['user_id']

def can_user_post(db, user_id):
	next_read = db.next_read(request['user_id'])
	if next_read < int(time.time()):
		return True

	return False


def main(db, request, consts):
	try:
		next_read = db.next_read(request['user_id'])
		seconds_left = next_read - int(time.time())

		return {
			'success' : True,
			'data' : {
				'can_post' : (seconds_left > 0),
				'when_will_post' : time.ctime(next_read)
			}
		}

	except Exception, e:
		return {
			'success' : False,
			'message' : e.message
		}

