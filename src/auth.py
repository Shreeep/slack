
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

    #Doesnt work yet

    #Checking for correct input
    for user in data['users']:
        if user['email'] == email:
            if user['password'] == password:
                ret = {
                    'u_id': userId,
                    'token': tokenId,
                }
                userId += 1
                tokenId += 1
                return ret
                

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    global userId
    global tokenId

    newUser = {
        'name_first': name_first,
        'name_last': name_last,
        'email': email,
        'password': password,
    }

    #Generating user handle and limiting to 20 chars
    handle = name_first.lower() + name_last.lower()
    handle = handle[:20]
    
    #checking if the handle has been used
    if handle in data['handles'] and len(handle) > 19:
        handle = handle[:-len(str(userId))] + str(userId)

    elif handle in data['handles']:
        handle = handle + str(userId - 1)

    #adding the registered user to global dict
    #adding the handle to the users dictionary?
    data['users'][userId] = {'handle' : handle}

    #checking if the handle has been used
    data['handles'][handle] = True

    ret =  {
        'u_id': userId,
        'token': tokenId,
    }

    userId += 1
    tokenId += 1

    return ret

# quick tests to see if it works
auth_register('test@email.com', 'password', 'Wilson', 'Guo')
print(data)
auth_register('test@email.com', 'password', 'Wilson', 'Guo')
print(data)
# auth_login('test@email.com', 'password')
# auth_register('test@email.com', 'password', 'anamethatismorethantwentychars', 'Lasdfas')
# print(data)
# auth_register('test@email.com', 'password', 'anamethatismorethantwentychars', 'Lasdfas')
# print(data)
