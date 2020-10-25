import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth
import channel
import channels
import other
import hashlib
import jwt
import data

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

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data_out = request.args.get('data')
    if data_out == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data_out
    })


@APP.route("/auth/register", methods=['POST'])
def register():
    # get the info
    user_info = request.get_json()

    # hash user password and register
    password = hashlib.sha256(user_info['password'].encode()).hexdigest()
    user = auth.auth_register(user_info['email'], password, user_info['name_first'], user_info['name_last'])

    # encoding jwt
    encoded_jwt = jwt.encode({'token': user['token']}, data.jwt_secret, algorithm='HS256')

    result = {
        'token': encoded_jwt.decode(),
        'u_id': user['u_id']
    }

    return dumps(result)
    

@APP.route("/auth/login", methods=['POST'])
def login():

    # get user info
    user_info = request.get_json()
    
    # hash user password and login
    password = hashlib.sha256(user_info['password'].encode()).hexdigest()
    user = auth.auth_login(user_info['email'], password)

    # encoding jwt
    encoded_jwt = jwt.encode({'token': user['token']}, data.jwt_secret, algorithm='HS256')

    result = {
        'token': encoded_jwt.decode(),
        'u_id': user['u_id']
    }

    return dumps(result)


@APP.route("/auth/logout", methods=['POST'])
def logout():

    # get user info
    user_info = request.get_json()

    # decode hashed jwt
    decoded_jwt = jwt.decode(user_info['token'], data.jwt_secret, algorithm='HS256')

    # logging out with token
    is_success = auth.auth_logout(decoded_jwt['token'])

    return dumps(is_success)

@APP.route("/users/all", methods=['GET'])
def users_all():

    # gets user info
    token = request.args['token']

    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')

    all_users = other.users_all(decoded_jwt['token'])

    return dumps({'users': all_users})

@APP.route("/channel/invite", methods=['POST'])
def invite():
    # get the info
    inv_data = request.get_json()
    decoded_jwt = jwt.decode(inv_data['token'], data.jwt_secret, algorithm='HS256')
    result = channel.channel_invite(decoded_jwt['token'], inv_data['channel_id'], inv_data['u_id'])

    return dumps(result)

@APP.route("/channel/details", methods=['GET'])
def details():
    # get the info
    token = request.args.get('token')
    channel_id = request.args.get('channel_id', default = 1, type = int)
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')

    result = channel.channel_details(decoded_jwt['token'], channel_id)

    return dumps(result)

@APP.route("/channel/messages", methods=['GET'])
def messages():
    # get the info
    token = request.args.get('token')
    channel_id = request.args.get('channel_id', default = 1, type = int)
    start = request.args.get('start')
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')

    result = channel.channel_messages(decoded_jwt['token'], channel_id['channel_id'], start)

    return dumps(result)

@APP.route("/channels/create", methods=['POST'])
def create():
    #Get channel info from front-end 
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    channel_id = channels.channels_create(decoded_jwt['token'], info['name'], info['is_public'])
    return dumps(channel_id)


if __name__ == "__main__":
    # APP.run(port=0) # Do not edit this port
    APP.run(port=0) # Do not edit this port

