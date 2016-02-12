from flask import Flask
from flask import request
import time
import os

import index_page.index as index_page


app = Flask(__name__)

@app.route("/test", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
def route_index():
	os.chdir('index_page')
    returned_data = index_page.main()
    os.chdir('..')
    return returned_data

def main():
	print 'started at {0}'.format(time.asctime())
