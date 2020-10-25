'''
@APP.route("/message/send", methods=['POST'])
def send_message():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    message = message.message_send(decoded_jwt['token'], info['channel_id'],  info['message'])
    result = {
        'message_id': message['message_id']
    }
    return dumps(result)

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

'''