import data
from error import InputError, AccessError

def clear():
    data.data['users'] = {}
    data.data['handles'] = {}
    data.data['tokens'] = {}
    data.data['channels'] = []
    data.token_id = 1
    data.user_id = 1

def users_all(token):

    if token not in data.data['tokens']:
        raise AccessError
    
    all_users = data.data['users'].values()

    for u in all_users:
        u.pop('password')
        u.pop('is_global_owner')

    return list(all_users)

def admin_userpermission_change(token, u_id, permission_id):
    pass

def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

# import auth
# import json
# auth.auth_register('test@email.com', 'password', 'test', 'user')
# auth.auth_register('test1@email.com', 'password', 'test', 'user')
# auth.auth_register('test2@email.com', 'password', 'test', 'user')
# auth.auth_register('test3@email.com', 'password', 'test', 'user')
# auth.auth_register('test4@email.com', 'password', 'test', 'user')
# # print(users_all('token1'))
# for u in users_all('token1'):
#     print (u)
