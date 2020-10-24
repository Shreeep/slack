import data
import re
from error import InputError, AccessError


def user_profile(token, u_id):
    
    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    # checking for valid u_id
    if u_id not in data.data['users']:
        raise InputError

    if data.data['tokens'][token] != u_id:
        raise AccessError

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
    if len(name_first) < data.MIN_NAME_LEN or len(name_first) > data.MAX_NAME_LEN: 
        raise InputError

    # last name is between 1 - 50
    if len(name_last) < data.MIN_NAME_LEN or len(name_last) > data.MAX_NAME_LEN:
        raise InputError

    user_id = data.data['tokens'][token]
    profile = data.data['users'][user_id]

    profile['name_first'] = name_first
    profile['name_last'] = name_last

    return {
    }

def user_profile_setemail(token, email):

    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    # checking for valid email
    if not re.search(data.EMAIL_REGEX,email):
        raise InputError

    # checking if email has been used
    for user in data.data['users']:
        if email == data.data['users'][user]['email']:
            raise InputError
       
    user_id = data.data['tokens'][token]
    profile = data.data['users'][user_id]

    profile['email'] = email

    return {
    }

def user_profile_sethandle(token, handle_str):

    # checking for valid token
    if token not in data.data['tokens']:
        raise AccessError

    if len(handle_str) > data.MAX_HANDLE_LEN or len(handle_str) < data.MIN_HANDLE_LEN:
        raise InputError

    # check if handle is used
    if handle_str in data.data['handles']:
        raise InputError
    
    # Saves the handle name
    user_id = data.data['tokens'][token]
    
    profile = data.data['users'][user_id]

    profile['handle_str'] = handle_str
    data.data['handles'][handle_str] = True

    return {
    }   




