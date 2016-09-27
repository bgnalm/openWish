from flask import Flask
from flask import request
import time
import os

import index_page.index as index_page
import add_wish.add_wish as add_wish
import create_user.create_user as create_user
import time_left.time_left as time_left
import read_wish.read_wish as read_wish
import get_wishes.get_wishes as get_wishes

import consts
import request_handler
from db import mongoInterface

app = Flask(__name__, static_folder='static')
db = mongoInterface.MongoInterface()

def load_static_page(path):
    try:
        html_file = open(path, 'r')
    except Exception ,e:
        return 'error: open {0}. {1}\n'.format(path, e) 

    html_text = html_file.read()
    html_file.close()
    return html_text

def process_json_api_call(module, usage_page):
    json_request = None

    try:
        json_request = request_handler.handle_json_request(
            request.data,
            module.REQUIRED_FIELDS
        )
    except request_handler.JsonRequestParsingError, e:
        return load_static_page(usage_page)
    except request_handler.NoRequiredFieldError, e:
        message = 'error. missing "{0}" in request. read the documentation at {1}'.format(e._field, usage_page)
        return request_handler.handle_response({'message': message, 'success':False})

    return request_handler.handle_response(module.main(db, json_request, consts))

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
    return process_json_api_call(add_wish, 'static/documentation/add_wish_usage.html')

@app.route("/readWish", methods=['POST', 'GET'])
@app.route("/read_wish", methods=['POST', 'GET'])
@app.route("/readwish", methods=['POST', 'GET'])
def route_read_wish():
    return process_json_api_call(read_wish, 'static/documentation/read_wish_usage.html')

@app.route("/createUser", methods=['POST', 'GET'])
@app.route("/create_user", methods=['POST' , 'GET'])
def route_create_user():
    return process_json_api_call(create_user, 'static/documentation/create_user_usage.html')

@app.route("/timeLeft", methods=['POST', 'GET'])
@app.route("/time_left", methods=['POST' , 'GET'])
def route_time_left():
    return process_json_api_call(time_left, 'static/documentation/time_left_usage.html')

@app.route("/getWishes", methods=['POST', 'GET'])
@app.route("/get_wishes", methods=['POST', 'GET'])
def route_get_wishes():
    return process_json_api_call(get_wishes, '')

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
