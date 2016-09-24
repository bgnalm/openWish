import time
import traceback

REQUIRED_FIELDS = ['user_name']

def can_user_post(db, user_name):
	user = db.load_user(user_name)
	return user._next_post_timestamp < time.time()

def can_user_read(db, user_name):
	user = db.load_user(user_name)
	return user._posts > user._reads

def main(db, request, consts):
	try:
		user = db.load_user(request['user_name'])
		return {
			'success' : True,
			'data' : {
				'can_read' : user._posts > user._reads,
				'can_post' : user._next_post_timestamp < time.time(),
				'next_post' : time.ctime(user._next_post_timestamp)
			}
		}

	except Exception, e:
		message = e.message
		if consts.FULL_TRACEBACK_MESSAGAE:
			message = traceback.format_exc()
		return {
			'success' : False,
			'message' : message
		}

