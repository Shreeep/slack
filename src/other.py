import data
from error import InputError, AccessError

def clear():
    data.data['users'] = {}
    data.data['handles'] = {}
    data.data['tokens'] = {}
    data.data['channels'] = []
    data.data['messages'] = []
    data.message_id = 1
    data.token_id = 1
    data.user_id = 1
    data.jwt_secret = "secret string"
    data.token_string = 'token'

def users_all(token):

    if token not in data.data['tokens']:
        raise AccessError
    
    all_users = data.data['users'].values()

    for u in all_users:
        u.pop('password')
        u.pop('is_global_owner')

    return list(all_users)

def admin_userpermission_change(token, u_id, permission_id):
    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    # checking for valid u_id
    if u_id not in data.data['users']:
        raise InputError

    # checking for valid permission_id
    if not permission_id in (1,2):
        raise InputError

    # checking if token user is global owner
    auth_u_id = data.data['tokens'][token]

    if not data.data['users'][auth_u_id]['is_global_owner']:
        raise AccessError
    
    # setting permission_id
    data.data['users'][u_id]['is_global_owner'] = (permission_id == 1)

    return {}

def search(token, query_str):
    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError
    
    u_id = data.data['tokens'][token]
    messages = []

    # checking for query string in user's channels
    for channel in data.data['channels']:
        if any(member['u_id'] == u_id for member in channel['members']):
            for message in channel['messages']:
                if (message['message'] == query_str):
                    messages.append(message)

    return {
        'messages': messages
    }
