import json
import time

def main(db, data, consts):
	"""
	example:
	{
		"user_id" : "bgnalm",
		"wish" : {
			"text" : " i wish there was more bars
			"optional" : {
				"city" : "rehovot",
			}
		}
	}
	"""

	json_request = None
	try:
		json_request = json.loads(data)

	except ValueError:
		return consts.REQUEST_JSON_PARSING_ERROR

	
	new_wish = consts.Wish(
		data.wish.text, 
		data.user_id, 
		optional=data.wish.optional
	)

	db.insert_wish(new_wish)

