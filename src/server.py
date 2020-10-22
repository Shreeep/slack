import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth
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

    password = hashlib.sha256(user_info['password'].encode()).hexdigest()
    user_token = auth.auth_register(user_info['email'], password, user_info['name_first'], user_info['name_last'])

    # print(f"AUTH REGISTER: {user_token}")

    encoded_jwt = jwt.encode(user_token, data.jwt_secret, algorithm='HS256')

    result = {
        'token': encoded_jwt.decode(),
        'u_id': user_token['u_id']
    }

    return result
    

@APP.route("/auth/login", methods=['POST'])
def login():

    # get user info
    user_info = request.get_json()
    
    # login
    password = hashlib.sha256(user_info['password'].encode()).hexdigest()
    user_token = auth.auth_login(user_info['email'], password)

    encoded_jwt = jwt.encode(user_token, data.jwt_secret, algorithm='HS256')

    result = {
        'token': encoded_jwt.decode(),
        'u_id': user_token['u_id']
    }

    return result


@APP.route("/auth/logout", methods=['POST'])
def logout():
    # check generated token?
    # decode generated token
    # check if decoded token matches DB?

    # get user info
    user_info = request.get_json()

    print(f"IN the logout function: {user_info}")

    decoded_jwt = jwt.decode(user_info['token'], data.jwt_secret, algorithm='HS256')

    isSuccess = auth.auth_logout(decoded_jwt['token'])

    return isSuccess

if __name__ == "__main__":
    # APP.run(port=0) # Do not edit this port
    APP.run(port=1337) # Do not edit this port
