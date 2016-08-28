import json
import time

REQUIRED_FIELDS = ['user_id', 'wish']

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
	}
	"""
	
	new_wish = consts.Wish(
		request.wish.text, 
		request.user_id,
		optional=request.wish.optional
	)

	try:
		return {
			'success' : True,
			'data' : {
				'wish_id' : db.insert_wish(new_wish)
			}
		}

	except Exception, e:
		return {
			'success' : False,
			'message' : e.message
		}



