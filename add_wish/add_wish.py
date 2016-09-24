import json
import time
import time_left.time_left
import traceback

REQUIRED_FIELDS = ['user_name', 'wish']

class UserCantPostError(Exception):
	pass

def main(db, request, consts):
	"""
	example:
	{
		"user_id" : "bgnalm",
		"wish" : {
			"text" : " i wish there were more bars
			"optional" : {
				"city" : "rehovot",
			}
		}
	}\
	"""

	new_wish = consts.Wish(
		request['wish']['text'],
		request['user_name'],
		optional=request['wish']['optional']
	)

	try:
		if not time_left.time_left.can_user_post(db, request['user_name']):
			raise UserCantPostError("User {0} cant post right now".format(request["user_name"]))

		return {
			'success' : True,
			'data' : {
				'wish_id' : str(db.insert_wish(new_wish))
			}
		}

	except Exception, e:
		message = e.message
		if consts.FULL_TRACEBACK_MESSAGAE:
			message = traceback.format_exc()
		return {
			'success' : False,
			'message' : traceback.message
		}



