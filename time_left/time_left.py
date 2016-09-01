import time

REQUIRED_FIELDS = ['user_name']

def can_user_post(db, user_name):
	user = db.load_user(user_name)
	return user._posts > user._reads

def main(db, request, consts):
	try:
		user = db.load_user(request['user_name'])
		return {
			'success' : True,
			'data' : {
				'can_read' :user._posts > user._reads,
				'next_post' : time.ctime(user._next_post_timestamp)
			}
		}

	except Exception, e:
		return {
			'success' : False,
			'message' : e.message
		}

