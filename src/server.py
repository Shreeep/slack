import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError
import auth
import channel
import channels
import message
import user
import other
import hashlib
import jwt
import data
import standup


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

APP = Flask(__name__, static_url_path='/static/')
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
    user1 = auth.auth_register(user_info['email'], password, user_info['name_first'], user_info['name_last'])

    # encoding jwt
    encoded_jwt = jwt.encode({'token': user1['token']}, data.jwt_secret, algorithm='HS256')

    result = {
        'token': encoded_jwt.decode(),
        'u_id': user1['u_id']
    }

    return dumps(result)
    

@APP.route("/auth/login", methods=['POST'])
def login():

    # get user info
    user_info = request.get_json()
    
    # hash user password and login
    password = hashlib.sha256(user_info['password'].encode()).hexdigest()
    user1 = auth.auth_login(user_info['email'], password)

    # encoding jwt
    encoded_jwt = jwt.encode({'token': user1['token']}, data.jwt_secret, algorithm='HS256')

    result = {
        'token': encoded_jwt.decode(),
        'u_id': user1['u_id']
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


@APP.route("/auth/passwordreset/request", methods=['POST'])
def auth_passwordreset_request():

    # get user info
    user_info = request.get_json()

    # request reset code
    auth.auth_passwordreset_request(user_info['email'])

    return dumps({})


@APP.route("/auth/passwordreset/reset", methods=['POST'])
def auth_passwordreset_reset():

    # get user info
    user_info = request.get_json()

    # reset password
    hashpw = hashlib.sha256(user_info['new_password'].encode()).hexdigest()
    auth.auth_passwordreset_reset(user_info['reset_code'], hashpw)

    return dumps({})


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
    channel_id = request.args.get('channel_id', default=1, type=int)
    star = request.args.get('start', default=0, type=int)
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')

    result = channel.channel_messages(decoded_jwt['token'], channel_id, star)

    return dumps(result)
    
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
def channel_list():
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
    channel_id = channels.channels_create(decoded_jwt['token'], info['name'], info['is_public'])
    return dumps(channel_id)

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
    return dumps({})

@APP.route("/message/edit", methods=['PUT'])
def edit_message():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    message.message_edit(decoded_jwt['token'], info['message_id'], info['message'])
    return dumps({})

@APP.route("/message/react", methods=['POST'])
def react_message():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    message.message_react(decoded_jwt['token'], info['message_id'],  info['react_id'])
    return dumps({})

@APP.route("/message/unreact", methods=['POST'])
def unreact_message():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    message.message_unreact(decoded_jwt['token'], info['message_id'],  info['react_id'])
    return dumps({})

@APP.route("/message/sendlater", methods=['POST'])
def send_message_later():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    user_message_sendlater = message.message_sendlater(decoded_jwt['token'], info['channel_id'], info['message'], info['time_sent'])
    return dumps(user_message_sendlater)

@APP.route("/message/pin", methods=['POST'])
def pin_message():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    message.message_pin(decoded_jwt['token'], info['message_id'])
    return dumps({})

@APP.route("/message/unpin", methods=['POST'])
def unpin_message():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    message.message_unpin(decoded_jwt['token'], info['message_id'])
    return dumps({})

@APP.route("/user/profile", methods=['GET'])
def profile():
    token = request.args['token']
    u_id = request.args.get('u_id', default = 0, type = int)
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    result = user.user_profile(decoded_jwt['token'], u_id)
    return dumps(result)

@APP.route("/user/profile/setname", methods=['PUT'])
def set_name():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    user.user_profile_setname(decoded_jwt['token'], info['name_first'], info['name_last'])
    return dumps({})

@APP.route("/user/profile/setemail", methods=['PUT'])
def set_email():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    user.user_profile_setemail(decoded_jwt['token'], info['email'])
    return dumps({})

@APP.route("/user/profile/sethandle", methods=['PUT'])
def set_handle():
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    user.user_profile_sethandle(decoded_jwt['token'], info['handle_str'])
    return dumps({})

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def user_profile_upload_photo():
    info = request.get_json()
    # check token
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    # upload user profile and crop
    user.user_profile_upload_photo(decoded_jwt['token'], info['img_url'], info['x_start'], info['y_start'], info['x_end'], info['y_end'])
    return dumps({})

@APP.route("/admin/userpermission/change", methods=['POST'])
def change():
    # get the info
    info = request.get_json()
    decoded_jwt = jwt.decode(info['token'], data.jwt_secret, algorithm='HS256')
    other.admin_userpermission_change(decoded_jwt['token'], info['u_id'], info['permission_id'])
    return dumps({})

@APP.route("/search", methods=['GET'])
def search():
    token = request.args['token']
    query_str = request.args['query_str']
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    result = other.search(decoded_jwt['token'], query_str)
    return dumps(result)

@APP.route("/clear", methods=['DELETE'])
def clear():
    other.clear()
    return dumps({})

@APP.route("/static/<path:path>")
def send_img(path):
    return send_from_directory('', path)

@APP.route("/standup/start", methods=['POST'])
def start():
    # get user info
    start_data = request.get_json()  
    decoded_jwt = jwt.decode(start_data['token'], data.jwt_secret, algorithm='HS256')
    result = standup.standup_start(decoded_jwt['token'], start_data['channel_id'], start_data['length'])
    return dumps(result)

@APP.route("/standup/active", methods=['GET'])
def active():
    token = request.args['token']
    channel_id = request.args.get('channel_id', default = 1, type = int)
    decoded_jwt = jwt.decode(token, data.jwt_secret, algorithm='HS256')
    result = standup.standup_active(decoded_jwt['token'], channel_id)
    return dumps(result)

@APP.route("/standup/send", methods=['POST'])
def send():
    # get user info
    send_data = request.get_json()  
    decoded_jwt = jwt.decode(send_data['token'], data.jwt_secret, algorithm='HS256')
    result = standup.standup_send(decoded_jwt['token'], send_data['channel_id'], send_data['message'])
    return dumps(result)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port

