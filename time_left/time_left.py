import time

REQUIRED_FIELDS = ['name']

def main(db, request, consts):
	next_read = db.next_read(request['name'])
	seconds_left = next_read - int(time.time())
	if seconds_left < 0:
		seconds_left = 0

	return str(seconds_left)

