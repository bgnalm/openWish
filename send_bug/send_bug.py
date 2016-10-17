import traceback
import time

REQUIRED_FIELDS = ['user_name', 'bug']

def main(db, request, consts):
	try:
		db.add_bug(request['bug'], request['user_name'], time.time())
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