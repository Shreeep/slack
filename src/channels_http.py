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
    return {'channels':user_channels}



@APP.route("/channels/listall", methods=['GET'])
def listall():
    token = request.args['token']
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    all_channels = channels.channels_listall(decoded_jwt['token'])
    return {'channels':all_channels}


@APP.route("/channels/create", methods=['POST'])
def create():
    #Get user info from front-end 
    info = request.get_json()
    channel = channels.channels_create(info['token'], info['name'], info['is_public'])
    result = {
        'channel_id': channel['channel_id']
    }
    return result 


if __name__ == "__main__":
    APP.run(port=5000) # Do not edit this port
   #APP.run(port=1337) # Do not edit this port