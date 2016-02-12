from flask import Flask
from flask import request
import time

import index_page.index as index_page


app = Flask(__name__)

@app.route("/test", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
def route_test():
    return index_page.main()

def main():
	print 'started at {0}'.format(time.asctime())
