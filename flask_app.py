from flask import Flask
from flask import request
import time
import os

import index_page.index as index_page
import add_wish.add_wish as add_wish


app = Flask(__name__)

@app.route("/test", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
def route_index():
    os.chdir('./index_page')
    returned_data = index_page.main()
    os.chdir('..')
    return returned_data    

@app.route("/addWish", methods['POST'])
@app.route("/add_wish", methods['POST'])
def route_add_wish():
    return add_wish.main()

def main():
    try:
        os.chdir('./openWish')
    except:
        pass

    app.run()  
    print 'started at {0}'.format(time.asctime())


if __name__ == "__main__":
    main()
