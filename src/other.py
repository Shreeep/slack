import data

def clear():
    data.data['users'] = {}
    data.data['handles'] = {}
    data.data['tokens'] = {}
    data.data['channels'] = []
    data.token_id = 1
    data.user_id = 1
    
def users_all(token):
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
        ],
    }

def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
<<<<<<< HEAD

=======
>>>>>>> origin/channel_test_shree
