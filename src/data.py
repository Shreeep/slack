
EMAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
MAX_HANDLE_LEN = 20
MIN_HANDLE_LEN = 3
MAX_NAME_LEN = 50
MIN_NAME_LEN = 1
MIN_PW_LEN = 6


#global variable to store the user data
data = {
    
    'users': {

    }, 
    
    'handles': {


	}, 

	'tokens': {


	},
    'channels': [],
}
jwt_secret = "secret string"
token_string = 'token'
token_id = 1
user_id = 1
message_id = 1