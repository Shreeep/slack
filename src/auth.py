
#global variable to store the user data
data = {
    
    'users': [] ,

}

tokenId = 1
userId = 1

def auth_login(email, password):

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

    newUser = {
        'name_first': name_first,
        'name_last': name_last,
        'email': email,
        'password': password,
    }

    #adding the registered user to global dict
    data['users'].append(newUser)

    #adding handle


    return {
        'u_id': userId,
        'token': tokenId,
    }

# quick tests to see if it works
def test_login():
    auth_register('test@email.com', 'password')
    assert auth_login('test@email.com', 'yes') == True
