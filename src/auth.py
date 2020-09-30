import re
import data

email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def auth_login(email, password):

    #checking if valid email
    if not re.search(email_regex,email):
        raise Exception(f"{email} is not valid")

    # Checking for correct input
    for user in data.data['users']:
        if data.data['users'][user]['email'] == email:
            if data.data['users'][user]['password'] == password:
                ret = {
                    'u_id': data.user_id,
                    'token': data.token_id,
                }

                data.user_id += 1
                data.token_id += 1
                return ret
            else:
                raise Exception(f"Password is incorrect")
                
    raise Exception(f"{email} is not registered")

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):

    #checking if valid email
    if not re.search(email_regex,email):
        raise Exception(f"{email} is not valid")

    #Generating user handle and limiting to 20 chars
    handle = name_first.lower() + name_last.lower()
    handle = handle[:20]
    
    #checking if the handle has been used
    if handle in data.data['handles'] and len(handle) >= 20:
        handle = handle[:-len(str(data.user_id))] + str(data.user_id)

    elif handle in data.data['handles']:
        handle = handle + str(data.user_id)

    #saving user info into a new dict
    new_user = {
        'email': email,
        'password': password,
        'handle': handle,
    }

    #adding user info to global dict
    data.data['users'][data.user_id] = new_user

    #Saves the handle name
    data.data['handles'][handle] = True

    ret =  {
        'u_id': data.user_id,
        'token': data.token_id,
    }

    data.user_id += 1
    data.token_id += 1

    return ret

