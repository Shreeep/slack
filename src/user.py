import data
import re
from error import InputError, AccessError

EMAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
MAX_NAME_LEN = 50
MIN_NAME_LEN = 1
MAX_HANDLE_LEN = 20
MIN_HANDLE_LEN = 3

def user_profile(token, u_id):
    
    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    # checking for valid u_id
    if u_id not in data.data['users']:
        raise InputError

    # if token != data.data['tokens'][u_id]:
    #     raise AccessError

    u_id = data.data['tokens'][token]
    profile = data.data['users'][u_id]

    profile.pop('password')
    profile.pop('is_global_owner')

    return profile

def user_profile_setname(token, name_first, name_last):

    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    # first name is between 1 - 50
    if len(name_first) < MIN_NAME_LEN or len(name_first) > MAX_NAME_LEN: 
        raise InputError

    # last name is between 1 - 50
    if len(name_last) < MIN_NAME_LEN or len(name_last) > MAX_NAME_LEN:
        raise InputError

    user_id = data.data['tokens'][token]
    profile = data.data['users'][user_id]

    profile['name_first'] = name_first
    profile['name_last'] = name_last

    # return profile
    return {
    }

def user_profile_setemail(token, email):

    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    # checking for valid email
    if not re.search(EMAIL_REGEX,email):
        raise InputError

    # checking if email has been used
    for user in data.data['users']:
        if email == data.data['users'][user]['email']:
            raise InputError
       
    user_id = data.data['tokens'][token]
    profile = data.data['users'][user_id]

    profile['email'] = email

    # return profile
    return {
    }

def user_profile_sethandle(token, handle_str):

    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    if len(handle_str) < MIN_HANDLE_LEN:
        raise InputError

    # # Generating user handle and limiting to 20 chars
    handle_str = handle_str[:MAX_HANDLE_LEN]
    
    # check if handle is used
    if handle_str in data.data['handles']:
        # limiting handle to handle length - user_id_length, then adding user_id to the end
        handle_str = handle_str[:MAX_HANDLE_LEN - len(str(data.user_id))] + str(data.user_id)
    
    # Saves the handle name

    user_id = data.data['tokens'][token]
    
    profile = data.data['users'][user_id]

    profile['handle_str'] = handle_str
    data.data['handles'][handle_str] = True

    return profile
    return {
    }   

# import auth
# # # import json
# auth.auth_register('test@email.com', 'password', 'test', 'user')
# auth.auth_register('test1@email.com', 'password', 'Another', 'user')
# print(auth.auth_register('test2@email.com', 'password', 'New', 'user'))
# # # auth.auth_register('test3@email.com', 'password', 'test', 'user')
# # # auth.auth_register('test4@email.com', 'password', 'test', 'user')
# # # print(user_profile('token3', 3))

# # print(user_profile_setname('token3', 'a', 'User'))
# # # print(user_profile_setemail('token3', 'newemail@email.com'))
# print(user_profile_sethandle('token3', 'testuser'))
# print(user_profile_sethandle('token2', 'abcdefghijklmnopqrstuvwyzabcdefghijklmnopqrstuvwyz'))
# print(user_profile_sethandle('token3', 'Anotheruser'))
# print(user_profile_sethandle('token2', 'abcdefghijklmnopqrstuvwyzabcdefghijklmnopqrstuvwyz'))
# print(user_profile_sethandle('token2', 'as'))
# print(data.data['handles'])



