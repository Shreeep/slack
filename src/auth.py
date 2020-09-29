import re

#global variable to store the user data
data = {
    
    'users': {

    },

    'handles' : {

    }

}

tokenId = 1
userId = 1

def auth_login(email, password):

    global userId
    global tokenId
    emailRegex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if not re.search(emailRegex,email):
        raise Exception(f"{email} is not valid")

    # Checking for correct input
    for user in data['users']:
        if data['users'][user]['email'] == email:
            if data['users'][user]['password'] == password:
                ret = {
                    'u_id': userId,
                    'token': tokenId,
                }

                userId += 1
                tokenId += 1
                return ret
            else:
                raise Exception(f"Password is incorrect")
                
    raise Exception(f"{email} is not registered")

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
   
    global userId
    global tokenId

    #Generating user handle and limiting to 20 chars
    handle = name_first.lower() + name_last.lower()
    handle = handle[:20]
    
    #checking if the handle has been used
    if handle in data['handles'] and len(handle) >= 20:
        handle = handle[:-len(str(userId))] + str(userId)

    elif handle in data['handles']:
        handle = handle + str(userId)

    #saving user info into a new dict
    newUser = {
        'email': email,
        'password': password,
        'handle': handle,
    }

    #adding user info to global dict
    data['users'][userId] = newUser

    #Saves the handle name
    data['handles'][handle] = True

    ret =  {
        'u_id': userId,
        'token': tokenId,
    }

    userId += 1
    tokenId += 1

    return ret

