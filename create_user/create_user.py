import traceback
import time

REQUIRED_FIELDS = ['user_name']

def main(db, request, consts):

	try:
		return {
			'success' : True,
			'data' : {
				'user_id' : str(db.create_user(request['user_name']))
			}
		}

	except Exception, e:
		return {
			'success' : False,
			'message' : traceback.format_exc()
		}