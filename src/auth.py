data = {
	'users': []	

}


def auth_login(email, password):

	for user in data['users']:
		if user['email'] == email:
			if user['password'] == password

				print("Success")
  
    return {
        'u_id': 1,
        'token': '12345',
    }


def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):

	newUser = {

		'email': email,
		'password': password,

	}

	data['users'].append(newUser)


    return {
        'u_id': 1,
        'token': '12345',
    }



