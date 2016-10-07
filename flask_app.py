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
import get_wish.get_wish as get_wish
import rate_wish.rate_wish as rate_wish

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

def process_json_api_call(module):
    json_request = None

    try:
        json_request = request_handler.handle_json_request(
            request.data,
            module.REQUIRED_FIELDS
        )
    except request_handler.JsonRequestParsingError, e:
        message = 'error in request, no JSON could be parsed'
        return request_handler.handle_response({'message':message, 'success':False})
    except request_handler.NoRequiredFieldError, e:
        message = 'missing field "{0}" in request'.format(e._field)
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
    return process_json_api_call(add_wish)

@app.route("/readWish", methods=['POST', 'GET'])
@app.route("/read_wish", methods=['POST', 'GET'])
@app.route("/readwish", methods=['POST', 'GET'])
def route_read_wish():
    return process_json_api_call(read_wish)

@app.route("/createUser", methods=['POST', 'GET'])
@app.route("/create_user", methods=['POST' , 'GET'])
def route_create_user():
    return process_json_api_call(create_user)

@app.route("/timeLeft", methods=['POST', 'GET'])
@app.route("/time_left", methods=['POST' , 'GET'])
def route_time_left():
    return process_json_api_call(time_left)

@app.route("/getWishes", methods=['POST', 'GET'])
@app.route("/get_wishes", methods=['POST', 'GET'])
def route_get_wishes():
    return process_json_api_call(get_wishes)

@app.route("/getWish", methods=['POST', 'GET'])
@app.route("/get_wish", methods=['POST', 'GET'])
def route_get_wish():
    return process_json_api_call(get_wish)

@app.route("/rateWish", methods=['POST', 'GET'])
@app.route("/rate_wish", methods=['POST', 'GET'])
def route_rate_wish():
    return process_json_api_call(rate_wish)

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
