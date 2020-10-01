import re
import data
from error import InputError, AccessError

email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def auth_login(email, password):

    #checking if valid email
    if not re.search(email_regex,email):
        raise InputError

    # Checking for correct input
    for user in data.data['users']:
        if data.data['users'][user]['email'] == email:
            if data.data['users'][user]['password'] == password:
                ret = {
                    'u_id': data.user_id,
                    'token': data.token_id,
                }

                # Adding to the token dictionary
                data.data['token'][data.token_id] = data.user_id

                data.user_id += 1
                data.token_id += 1
                return ret
            else:
                raise InputError
                
    raise InputError

def auth_logout(token):

    # for token in data.data['token']:
    if token in data.data['token']:
        data.data['token'].pop(token)
        return {
            'is_success': True,
        }
    else:
        return {
            'is_success': False,
        }

def auth_register(email, password, name_first, name_last):

    # checking if valid email
    if not re.search(email_regex,email):
        raise InputError

    # Generating user handle and limiting to 20 chars
    handle = name_first.lower() + name_last.lower()
    handle = handle[:20]
    
    #checking if the handle has been used
    if handle in data.data['handles'] and len(handle) >= 20:
        handle = handle[:-len(str(data.user_id))] + str(data.user_id)

    elif handle in data.data['handles']:
        handle = handle + str(data.user_id)

    # saving user info into a new dict
    new_user = {
        'email': email,
        'password': password,
        'handle': handle,
    }

    # checking whether the email has been registered before
    for user in data.data['users']:
        if new_user['email'] == data.data['users'][user]['email']:
            raise InputError

    # Checking whether the password is valid
    if len(new_user['password']) < 7:
        raise InputError

    # first name is between 1 - 50
    if len(name_first) < 1 or len(name_first) > 50: 
        raise InputError

    # last name is between 1 - 50
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError

    # adding user info to global dict
    data.data['users'][data.user_id] = new_user

    # Saves the handle name
    data.data['handles'][handle] = True

    ret =  {
        'u_id': data.user_id,
        'token': data.token_id,
    }

    # Adding to the token dictionary
    data.data['token'][data.token_id] = data.user_id

    data.user_id += 1
    data.token_id += 1

    return ret

