import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth
import channels
import channel
import message
import other
import hashlib
import jwt
import data
import channel

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
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
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

    return result
    

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

    return result


@APP.route("/auth/logout", methods=['POST'])
def logout():

    # get user info
    user_info = request.get_json()

    # decode hashed jwt
    decoded_jwt = jwt.decode(user_info['token'], data.jwt_secret, algorithm='HS256')

    # logging out with token
    is_success = auth.auth_logout(decoded_jwt['token'])

    return is_success

@APP.route("/users/all", methods=['GET'])
def users_all():

    # gets user info
    token = request.args['token']

    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')

    all_users = other.users_all(decoded_jwt['token'])

    return {'users': all_users}
    
@APP.route("/channel/leave", methods=['POST'])
def leave():
    # get user info
    leave_data = request.get_json()  
    decoded_jwt = jwt.decode(leave_data['token'], data.jwt_secret, algorithm='HS256')
    result = channel.channel_leave(decoded_jwt['token'], leave_data['channel_id'])

    return dumps(result)

@APP.route("/channel/join", methods=['POST'])
def join():
    # get user info
    join_data = request.get_json()  
    decoded_jwt = jwt.decode(join_data['token'], data.jwt_secret, algorithm='HS256')
    result = channel.channel_join(decoded_jwt['token'], join_data['channel_id'])

    return dumps(result)

@APP.route("/channel/addowner", methods=['POST'])
def addowner():
    # get user info
    add_data = request.get_json()
    decoded_jwt = jwt.decode(add_data['token'], data.jwt_secret, algorithm='HS256')
    result = channel.channel_addowner(decoded_jwt['token'], add_data['channel_id'], add_data['u_id'])
    return dumps(result)

@APP.route("/channel/removeowner", methods=['POST'])
def removeowner():
    # get user info
    remove_data = request.get_json()
    decoded_jwt = jwt.decode(remove_data['token'], data.jwt_secret, algorithm='HS256')
    result = channel.channel_removeowner(decoded_jwt['token'], remove_data['channel_id'], remove_data['u_id'])
    return dumps(result)

@APP.route("/channels/list", methods=['GET'])
def list():
    token = request.args['token']
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    user_channels = channels.channels_list(decoded_jwt['token'])
    return dumps(user_channels)


@APP.route("/channels/listall", methods=['GET'])
def listall():
    token = request.args['token']
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    all_channels = channels.channels_listall(decoded_jwt['token'])
    return dumps(all_channels)


@APP.route("/channels/create", methods=['POST'])
def create():
    #Get channel info from front-end 
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    channel = channels.channels_create(decoded_jwt['token'], info['name'], info['is_public'])
    return dumps(channel)

@APP.route("/message/send", methods=['POST'])
def send_message():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    user_message = message.message_send(decoded_jwt['token'], info['channel_id'],  info['message'])
    return dumps(user_message)

@APP.route("/message/remove", methods=['DELETE'])
def remove_message():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    message.message_remove(decoded_jwt['token'], info['message_id'])
    return {}

@APP.route("/message/edit", methods=['PUT'])
def edit_message():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    message.message_edit(decoded_jwt['token'], info['message_id'], info['message'])
    return {}

if __name__ == "__main__":
    #APP.run(port=0) # Do not edit this port
    APP.run(port=1337) # Do not edit this port
