import re
import data
from error import InputError, AccessError

email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def auth_login(email, password):

    # Checking if valid email
    if not re.search(email_regex,email):
        raise InputError

    # Checking for correct input
    # Loop through the data dictionary
    for user in data.data['users']:
        # Checks the data dictionary for the correct email and password
        if data.data['users'][user]['email'] == email:
            if data.data['users'][user]['password'] == password:
                token = data.token_string + str(data.token_id)

                ret = {
                    'u_id': user,
                    'token': token,
                }

                # Adds to the token dictionary
                data.data['token'][token] = user

                data.user_id += 1
                data.token_id += 1
                return ret
            else:
                # Password is incorrect
                raise InputError

    # Email not found in the data
    raise InputError

def auth_logout(token):

    # Checking if the token exists
    if token in data.data['token']:
        # Remove the token from the token dictionary
        data.data['token'].pop(token)
        return {
            'is_success': True,
        }
    else:
        # Invalid token
        raise AccessError

def auth_register(email, password, name_first, name_last):

    # Checking if valid email
    if not re.search(email_regex,email):
        raise InputError

    # Generating user handle and limiting to 20 chars
    handle = name_first.lower() + name_last.lower()
    handle = handle[:20]

    # checking if the handle has been used
    # make sure handle is within 20 chars after making handle unique
    if handle in data.data['handles'] and len(handle) >= 20:
        handle = handle[:-len(str(data.user_id))] + str(data.user_id)

    elif handle in data.data['handles']:
        handle = handle + str(data.user_id)

    # Checking if the dictionary is empty
    # make the first registered user in the dictionary global owner
    is_global_owner = False
    if len(data.data['users']) == 0:
        is_global_owner = True

    # saving new user info into a new dict
    new_user = {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
        'is_global_owner': is_global_owner
    }

    # checking whether the email has been registered before
    for user in data.data['users']:
        if new_user['email'] == data.data['users'][user]['email']:
            raise InputError

    # Checking whether the password is valid
    if len(new_user['password']) < 6:
        raise InputError

    # first name is between 1 - 50
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError

    # last name is between 1 - 50
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError

    # adding new user info to global data dict
    data.data['users'][data.user_id] = new_user

    # Saves the handle name
    data.data['handles'][handle] = True

    # making unique token
    token = data.token_string + str(data.token_id)

    ret =  {
        'u_id': data.user_id,
        'token': token,
    }

    # Adding to the token dictionary
    data.data['token'][token] = data.user_id

    data.user_id += 1
    data.token_id += 1

    return ret
