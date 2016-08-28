from flask import Flask
from flask import request
import time
import os

import index_page.index as index_page
import add_wish.add_wish as add_wish
import create_user.create_user as create_user
import time_left.time_left as time_left

import consts
import request_handler
from db import mongoInterface


app = Flask(__name__)
db = mongoInterface.MongoInterface()

def load_static_page(path):
    try:
        html_file = open(path, 'r')
    except Exception ,e:
        return 'error: open {0}. {1}\n'.format(path, e) 

    html_text = html_file.read()
    html_file.close()
    return html_text

@app.route("/test", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
def route_index():
    os.chdir('./index_page')
    returned_data = index_page.main(consts)
    os.chdir('..')
    return returned_data    

@app.route("/addWish", methods=['POST', 'GET'])
@app.route("/add_wish", methods=['POST', 'GET'])
def route_add_wish():
    json_request = None

    try:
        json_request = request_handler.handle_json_request(
            request.data,
            add_wish.REQUIRED_FIELDS
        )
    except:
        return load_static_page('add_wish/add_wish_usage.html')

    return request_handler.handle_response(add_wish.main(db, json_request, consts))

@app.route("/createUser", methods=['POST', 'GET'])
@app.route("/create_user", methods=['POST' , 'GET'])
def route_create_user():
    json_request = None

    try:
        json_request = request_handler.handle_json_request(
            request.data,
            create_user.REQUIRED_FIELDS
        )
    except:
        return load_static_page('create_user/create_user_usage.html')

    return request_handler.handle_response(create_user.main(db, json_request, consts))

@app.route("/timeLeft", methods=['POST', 'GET'])
@app.route("/time_left", methods=['POST' , 'GET'])
def route_time_left():
    json_request = None

    try:
        json_request = request_handler.handle_json_request(
            request.data,
            time_left.REQUIRED_FIELDS
        )
    except:
        return load_static_page('time_left/time_left_usage.html')

    return request_handler.handle_response(time_left.main(db, json_request, consts))

def main():
    try:
        os.chdir('./openWish')
    except:
        pass

    print 'started at {0}'.format(time.asctime())
    app.debug = True
    app.run()  
    print 'ended at {0}'.format(time.asctime())


if __name__ == "__main__":
    main()
