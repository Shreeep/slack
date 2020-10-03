import channel
import auth
import channels
import pytest
import data
import error

def test_channel_invite_success():
    user1 = auth.auth_register('user12@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user22@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    user3 = auth.auth_register('userwabi@gmail.com', '123abc!@#', 'Richard', 'Dawkins')
    public_channel_id = channels.channels_create(user1['token'],"channel12",1)
    with pytest.raises(AccessError) as e:
        channel.channel_invite(user2['token'],public_channel_id,user3['u_id'])
    channel.channel_invite(user1['token'],public_channel_id,user2['u_id'])
    channel.channel_invite(user2['token'],public_channel_id,user3['u_id'])

def test_channel_invite_failure():
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user23@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    public_channel_id = channels.channels_create(user1['token'],"channel13",1)
    with pytest.raises(AccessError) as e:
        channel.channel_invite(user2['token'],public_channel_id,user1['u_id'])
    with pytest.raises(InputError) as e:
        channel.channel_invite(user1['token'],public_channel_id,25)
        channel.channel_invite(user1['token'],25,25)

def test_channel_details_success():
    user1 = auth.auth_register('user14@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user24@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    public_channel_id = channels.channels_create(user1['token'],"channel14",1)
    assert channel.channel_details(user1['token'],public_channel_id) == {
        'name': 'channel14',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def test_channel_details_failure():
    user1 = auth.auth_register('user15@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user25@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    public_channel_id = channels.channels_create(user1['token'],"channel15",1)
    with pytest.raises(AccessError) as e:
        channel.channel_details(user2['token'],public_channel_id)
    with pytest.raises(InputError) as e:
        channel.channel_details(user1['token'],25)

def test_channel_messages_success():
    user1 = auth.auth_register('user16@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user26@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    public_channel_id = channels.channels_create(user1['token'],"channel16",1)
    for chan in data.data['channels']:
        if public_channel_id == chan['id']:
            chan['messages'] = [
                    {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                    },
                    {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'Hello world1',
                    'time_created': 1582426790,
                    },
                ]
            result = chan['messages']
    assert channel.channel_messages(user1['token'],public_channel_id,0) == {
        'messages': result,
        'start': 0,
        'end': -1,
    }

def test_channel_messages_failure():
    user1 = auth.auth_register('user17@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user27@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    public_channel_id = channels.channels_create(user1['token'],"channel17",1)
    for chan in data.data['channels']:
        if public_channel_id == chan['id']:
            chan['messages'] = [
                    {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                    },
                    {
                    'message_id': 2,
                    'u_id': 1,
                    'message': 'Hello world1',
                    'time_created': 1582426790,
                    },
                ]
    with pytest.raises(AccessError) as e:
        channel.channel_messages(user2['token'],public_channel_id,0)
    with pytest.raises(InputError) as e:
        channel.channel_messages(user1['token'],25,0)
        channel.channel_messages(user1['token'],public_channel_id,30)