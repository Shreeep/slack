data = {
    'users': {
        1: {
            'email': 'asdas@gmail.com',
            'password': 'password',
            'name_first': 'Richard',
            'name_last': 'Wilkinson',
            'handle_str': 'handle',
            'is_global_owner' : True
        },
        2: {
            'email': 'asd2r2as@gmail.com',
            'password': 'pas2234sword',
            'name_first': 'bob',
            'name_last': 'jane',
            'handle_str': 'handler',
            'is_global_owner' : False
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
            'members' : [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                },
            ],
            'owners' : [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                }
            ],
            'is_public': False,
        },
    ],
    'tokens': {
        'token1': 1, #userid
        'token2': 2,
    },
}