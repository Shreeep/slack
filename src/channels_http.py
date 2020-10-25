'''
import channels
import json
from echo_http_test import url 
import socketserver
import data
from flask import Flask, request 
import jwt

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

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

@APP.route("/channels/list", methods=['GET'])
def list():
    token = request.args['token']
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    user_channels = channels.channels_list(decoded_jwt['token'])
    return json.dumps(user_channels)



@APP.route("/channels/listall", methods=['GET'])
def listall():
    token = request.args['token']
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    all_channels = channels.channels_listall(decoded_jwt['token'])
    return json.dumps(all_channels)


@APP.route("/channels/create", methods=['POST'])
def create():
    #Get channel info from front-end 
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    return json.dumps(channels.channels_create(decoded_jwt['token'], info['name'], info['is_public']))



if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
   #APP.run(port=1337) # Do not edit this port

'''