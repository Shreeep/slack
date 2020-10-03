data = {
    'users': {
        1: {
            'email': 'asdas@gmail.com',
            'password': 'password',
            'name_first': 'name_first',
            'name_last': 'name_last',
            'handle_str': 'handle',
            'is_global_owner' : True
        },
        2: {
            'email': 'email@poomail.com',
            'password': 'password',
            'name_first': 'name_first',
            'name_last': 'name_last',
            'handle_str': 'handle',
            'is_global_owner': False
        },
    },
    'channels': [
        {
            'id': 1,
            'name' : 'channel1',
            #user1, user2, user3
            'members' : [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                },
                {
                    'u_id': 2,
                    'name_first': 'Bob',
                    'name_last': 'Willy',
                }
            ],
            'owners' : [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                }
            ],
            'is_public': True,
        },
        {
            'id': 2,
            'name' : 'channel2',
            #user1, user2, user3
            'members' : [1, 2, 3],
            'owners' : [3, 4],
            'is_public': True,
        },
    ],
    'tokens': {
        'token1': 523, #userid
        'token2': 1234,
    },
}