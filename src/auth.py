import re
import data
from error import InputError, AccessError


def auth_login(email, password):

    # Checking if valid email
    if not re.search(data.EMAIL_REGEX,email):
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
                data.data['tokens'][token] = user

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
    if token in data.data['tokens']:
        # Remove the token from the token dictionary
        data.data['tokens'].pop(token)
        return {
            'is_success': True,
        }
    else:
        # Invalid token
        raise AccessError

def auth_register(email, password, name_first, name_last):

    # Checking if valid email
    if not re.search(data.EMAIL_REGEX,email):
        raise InputError

    # Generating user handle and limiting to 20 chars
    handle = name_first.lower() + name_last.lower()
    handle = handle[:data.MAX_HANDLE_LEN]
    
    # if the handle has been used
    if handle in data.data['handles']:
        # limiting handle to handle length - user_id_length, then adding user_id to the end
        handle = handle[:data.MAX_HANDLE_LEN - len(str(data.user_id))] + str(data.user_id)

    # Checking if the dictionary is empty
    # make the first registered user in the dictionary global owner
    is_global_owner = False
    if len(data.data['users']) == 0:
        is_global_owner = True

    # saving new user info into a new dict
    new_user = {
        'u_id': data.user_id,
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
    if len(new_user['password']) < data.MIN_PW_LEN:
        raise InputError

    # first name is between 1 - 50
    if len(name_first) < data.MIN_NAME_LEN or len(name_first) > data.MAX_NAME_LEN: 
        raise InputError

    # last name is between 1 - 50
    if len(name_last) < data.MIN_NAME_LEN or len(name_last) > data.MAX_NAME_LEN:
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
    data.data['tokens'][token] = data.user_id

    data.user_id += 1
    data.token_id += 1

    return ret


def auth_passwordreset_request(email):

    # Checking if valid email
    if not re.search(data.EMAIL_REGEX,email):
        raise InputError

    all_users = data.data['users'].values()

    # check the entered email is an email saved in the data
    for user in all_users:
        if email in user['email']:
            
            # generate reset code
            reset_code = user['email'] + user['password']

            # storing reset code
            data.data['reset_code'][reset_code] = user['u_id']

  
def auth_passwordreset_reset(reset_code, new_password):

    if len(new_password) < data.MIN_PW_LEN:
        raise InputError

    if reset_code in data.data['reset_code']:
        u_id = data.data['reset_code'][reset_code]
        data.data['users'][u_id]['password'] = new_password

    else:
        raise InputError

