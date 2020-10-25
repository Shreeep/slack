import channel
import json
from echo_http_test import url
import server
# import data
from flask import Flask, request
import jwt
import data


@APP.route("/channel/leave", methods=['POST'])
def leave():
    # get user info
    token = request.args['token']  
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    channel = request.args['channel_id']

    result = channel.channel_leave(decoded_jwt['token'], channel)

    return dumps(result)


@APP.route("/channel/join", methods=['POST'])
def join():
    # get user info
    token = request.args['token']  
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    channel = request.args['channel_id']

    result = channel.channel_join(decoded_jwt['token'], channel)
    return dumps(result)


@APP.route("/channel/addowner", methods=['POST'])
def addowner():
    # get user info
    token = request.args['token']  
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    channel = request.args['channel_id']
    user_id = request.args['u_id']

    result = channel.channel_addowner(decoded_jwt['token'], channel, user_id)
    return dumps(result)


@APP.route("/channel/removeowner", methods=['POST'])
def removeowner():
    # get user info
    token = request.args['token']  
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    channel = request.args['channel_id']
    user_id = request.args['u_id']

    result = channel.channel_removeowner(decoded_jwt['token'], channel, user_id)

    return dumps(result)

