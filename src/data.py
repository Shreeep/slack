data = {
        'users': {
            1: {
                'id': 1,
                'name' : 'user1',
                'token': 'fasr',
            },
            2: {
                'id': 2,
                'name' : 'user2',
                'token' : 'asdfasdv',
            },
        },
        'channels': [
            {
                'id': 1,
                'name' : 'channel1',
                #user1, user2, user3
                'members' : '',
                'owners' : '',
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
            'token1': 523,
            'token2': 1234,
        },
    }