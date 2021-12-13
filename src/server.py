import jwt
import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from scrape import getValidGGST, overview


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path='/static/cropped')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    # if data == 'echo':
   	#     raise 'Cannot echo "echo"'
    return dumps({
        'data': data
    })

@APP.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@APP.route("/character", methods=['GET'])
def character_getJSON():
    payload = request.args.get('payload')
    if payload in getValidGGST():
        character = payload
        url = f"https://www.dustloop.com/wiki/index.php?title=GGST/{character}" 
    else:
        # assuming url page payload
        url = payload
    return dumps(overview(url))


if __name__=="__main__":
    APP.run(port=5050)