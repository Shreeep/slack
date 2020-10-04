import channel
import auth
import channels
import pytest
import data
import other
from error import InputError, AccessError
from datetime import datetime

def test_channel_invite_success():
    # clearing data
    other.clear()
    # registering 3 users
    user1 = auth.auth_register('user12@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user22@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    user3 = auth.auth_register('userwabi@gmail.com', '123abc!@#', 'Richard', 'Dawkins')
    # creating channel with user 1
    public_channel_id = channels.channels_create(user1['token'],"channel12",1)
    # checking if user 2 can invite user 3 yet
    # should fail as user 2 is not in the channel
    with pytest.raises(AccessError) as e:
        channel.channel_invite(user2['token'],public_channel_id['channel_id'],user3['u_id'])
    # inviting user 2 to channel
    channel.channel_invite(user1['token'],public_channel_id['channel_id'],user2['u_id'])
    # user 2 can now add user 3 to channel
    channel.channel_invite(user2['token'],public_channel_id['channel_id'],user3['u_id'])

def test_channel_invite_failure_wrong_inputs():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user23@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # creating channel with user 1
    public_channel_id = channels.channels_create(user1['token'],"channel13",1)
    with pytest.raises(InputError) as e:
        # give invalid u_id (user doesn't exist)
        channel.channel_invite(user1['token'],public_channel_id['channel_id'],25)
        # give invalid channel_id as channel doesnt exist
        channel.channel_invite(user1['token'],25,25)

def test_channel_invite_failure_access_errors():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user23@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # creating channel with user 1
    public_channel_id = channels.channels_create(user1['token'],"channel13",1)
    with pytest.raises(AccessError) as e:
        # user 2 is not in the channel yet
        channel.channel_invite(user2['token'],public_channel_id['channel_id'],user1['u_id'])
        # invalid token
        channel.channel_invite('faweebawoowaba' + user2['token'],public_channel_id['channel_id'],user1['u_id'])

def test_channel_details_success_two_users():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user14@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user24@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # creating channel with user 1 and inviting user 2
    public_channel_id = channels.channels_create(user1['token'],"channel14",1)
    channel.channel_invite(user1['token'],public_channel_id['channel_id'],user2['u_id'])
    # checking for correct output
    assert channel.channel_details(user1['token'],public_channel_id['channel_id']) == {
        'name': 'channel14',
        'owner_members': [
            {
                'u_id': user1['u_id'],
                'name_first': 'Hayden',
                'name_last': 'Everest',
            },
            {
                'u_id': user2['u_id'],
                'name_first': 'Bowen',
                'name_last': 'Pierce',
            }
        ],
        'all_members': [
            {
                'u_id': user1['u_id'],
                'name_first': 'Hayden',
                'name_last': 'Everest',
            },
            {
                'u_id': user2['u_id'],
                'name_first': 'Bowen',
                'name_last': 'Pierce',
            }
        ],
    }

def test_channel_details_failure_wrong_input():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user15@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user25@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # creating channel with user 1
    public_channel_id = channels.channels_create(user1['token'],"channel15",1)
    # error from entering wrong channel id
    with pytest.raises(InputError) as e:
        channel.channel_details(user1['token'],25)

def test_channel_details_failure_access_erros():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user15@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user25@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # creating channel with user 1
    public_channel_id = channels.channels_create(user1['token'],"channel15",1)
    with pytest.raises(AccessError) as e:
        # user2 is not in the channel
        channel.channel_details(user2['token'],public_channel_id['channel_id'])
        # invalid token
        channel.channel_invite('faweebawoowaba' + user2['token'],public_channel_id['channel_id'],user1['u_id'])

def test_channel_messages_failure_no_msgs():
    # clearing data
    other.clear()
    # registering a user
    user1 = auth.auth_register('user16@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    # user1 creates a channel
    public_channel_id = channels.channels_create(user1['token'],"channel16",1)
    # error as start index is 0 but messages is empty as no msgs sent
    with pytest.raises(InputError) as e:
        assert channel.channel_messages(user1['token'],public_channel_id['channel_id'],0)

def test_channel_messages_failure_wrong_input():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user17@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user27@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # user 1 creates a channel
    public_channel_id = channels.channels_create(user1['token'],"channel17",1)
    with pytest.raises(InputError) as e:
        # puts in invalid channel_id
        channel.channel_messages(user1['token'],25,0)
        # puts in invalid start index
        channel.channel_messages(user1['token'],public_channel_id['channel_id'],30)

def test_channel_messages_failure_access_errors():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user17@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user27@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # user 1 creates a channel
    public_channel_id = channels.channels_create(user1['token'],"channel17",1)
    with pytest.raises(AccessError) as e:
        # user2 is not in the channel
        channel.channel_messages(user2['token'],public_channel_id['channel_id'],0)
        # invalid token
        channel.channel_invite('faweebawoowaba' + user2['token'],public_channel_id['channel_id'],user1['u_id'])

# def test_channel_messages_success_25_msgs():
#     other.clear()
#     user1 = auth.auth_register('user16@gmail.com', '123abc!@#', 'Hayden', 'Everest')
#     user2 = auth.auth_register('user26@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
#     public_channel_id = channels.channels_create(user1['token'],"channel16",1)
#     channel.channel_invite(user1['token'],public_channel_id['channel_id'],user2['u_id'])
#     messages = []
#     for i in range(25):
#         message.message_send(user1['token'],public_channel_id['channel_id'],'testing123')
#         messages.append({
#             'message_id': i + 1,
#             'u_id': user1['u_id'],
#             'message': 'testing123',
#             'time_created': datetime.now(),
#         })
#     assert channel.channel_messages(user1['token'],public_channel_id['channel_id'],0) == {
#         'messages': messages,
#         'start': 0,
#         'end': -1,
#     }

# def test_channel_messages_success_50_msgs():
#     other.clear()
#     user1 = auth.auth_register('user16@gmail.com', '123abc!@#', 'Hayden', 'Everest')
#     user2 = auth.auth_register('user26@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
#     public_channel_id = channels.channels_create(user1['token'],"channel16",1)
#     channel.channel_invite(user1['token'],public_channel_id['channel_id'],user2['u_id'])
#     messages = []
#     for i in range(50):
#         message.message_send(user1['token'],public_channel_id['channel_id'],'testing123')
#         messages.append({
#             'message_id': i + 1,
#             'u_id': user1['u_id'],
#             'message': 'testing123',
#             'time_created': datetime.now(),
#         })
#     assert channel.channel_messages(user1['token'],public_channel_id['channel_id'],0) == {
#         'messages': messages,
#         'start': 0,
#         'end': 50,
#     }

# def test_channel_messages_success_embedded_msgs():
#     other.clear()
#     user1 = auth.auth_register('user16@gmail.com', '123abc!@#', 'Hayden', 'Everest')
#     user2 = auth.auth_register('user26@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
#     public_channel_id = channels.channels_create(user1['token'],"channel16",1)
#     for chan in data.data['channels']:
#         if public_channel_id['channel_id'] == chan['id']:
#             chan['messages'] = [
#                     {
#                     'message_id': 1,
#                     'u_id': 1,
#                     'message': 'Hello world',
#                     'time_created': 1582426789,
#                     },
#                     {
#                     'message_id': 2,
#                     'u_id': 1,
#                     'message': 'Hello world1',
#                     'time_created': 1582426790,
#                     },
#                 ]
#             result = chan['messages']
#     assert channel.channel_messages(user1['token'],public_channel_id['channel_id'],0) == {
#         'messages': result,
#         'start': 0,
#         'end': -1,
#     }