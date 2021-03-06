import channel
import auth
import channels
import pytest
import data
import other
import message
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
    public_channel_id2 = channels.channels_create(user1['token'],"channel123",1)
    # checking if user 2 can invite user 3 yet
    # should fail as user 2 is not in the channel
    with pytest.raises(AccessError):
        channel.channel_invite(user2['token'],public_channel_id['channel_id'],user3['u_id'])
    # inviting user 2 to channel
    channel.channel_invite(user1['token'],public_channel_id['channel_id'],user2['u_id'])
    channel.channel_invite(user1['token'],public_channel_id['channel_id'],user2['u_id'])
    # user 2 can now add user 3 to channel
    channel.channel_invite(user2['token'],public_channel_id['channel_id'],user3['u_id'])
    # inviting user 2 to channel
    channel.channel_invite(user1['token'],public_channel_id2['channel_id'],user2['u_id'])
    # user 2 can now add user 3 to channel
    channel.channel_invite(user2['token'],public_channel_id2['channel_id'],user3['u_id'])

def test_channel_invite_failure_wrong_inputs():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user23@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # creating channel with user 1
    public_channel_id = channels.channels_create(user1['token'],"channel13",1)
    with pytest.raises(InputError):
        # give invalid u_id (user doesn't exist)
        channel.channel_invite(user1['token'],public_channel_id['channel_id'],25)
    with pytest.raises(InputError):
        # give invalid channel_id as channel doesnt exist
        channel.channel_invite(user1['token'],25,user2['u_id'])

def test_channel_invite_failure_access_errors():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user23@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # creating channel with user 1
    public_channel_id = channels.channels_create(user1['token'],"channel13",1)
    with pytest.raises(AccessError):
        # user 2 is not in the channel yet
        channel.channel_invite(user2['token'],public_channel_id['channel_id'],user1['u_id'])
    with pytest.raises(AccessError):
        # invalid token
        channel.channel_invite('faweebawoowaba' + user2['token'],public_channel_id['channel_id'],user1['u_id'])

def test_channel_details_success_two_users():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user14@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user24@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # creating channel with user 1 and inviting user 2
    channels.channels_create(user1['token'],"channel14",1)
    public_channel_id2 = channels.channels_create(user1['token'],"channel15",1)
    channels.channels_create(user1['token'],"channel16",1)
    channel.channel_invite(user1['token'],public_channel_id2['channel_id'],user2['u_id'])
    # checking for correct output
    assert channel.channel_details(user1['token'],public_channel_id2['channel_id']) == {
        'name': 'channel15',
        'owner_members': [
            {
                'u_id': user1['u_id'],
                'name_first': 'Hayden',
                'name_last': 'Everest',
                'profile_img_url': '',
            },
        ],
        'all_members': [
            {
                'u_id': user1['u_id'],
                'name_first': 'Hayden',
                'name_last': 'Everest',
                'profile_img_url': '',
            },
            {
                'u_id': user2['u_id'],
                'name_first': 'Bowen',
                'name_last': 'Pierce',
                'profile_img_url': '',
            }
        ],
    }

def test_channel_details_failure_wrong_input():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user15@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register('user25@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # creating channel with user 1
    channels.channels_create(user1['token'],"channel15",1)
    # error from entering wrong channel id
    with pytest.raises(InputError):
        channel.channel_details(user1['token'],25)

def test_channel_details_failure_access_erros():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user15@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user25@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # creating channel with user 1
    public_channel_id = channels.channels_create(user1['token'],"channel15",1)
    with pytest.raises(AccessError):
        # user2 is not in the channel
        channel.channel_details(user2['token'],public_channel_id['channel_id'])
    with pytest.raises(AccessError):
        # invalid token
        channel.channel_details('faweebawoowaba' + user2['token'],public_channel_id['channel_id'])

def test_channel_messages_failure_wrong_start_msgs():
    # clearing data
    other.clear()
    # registering a user
    user1 = auth.auth_register('user16@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    # user1 creates a channel
    public_channel_id = channels.channels_create(user1['token'],"channel16",1)
    public_channel_id = channels.channels_create(user1['token'],"channel15",1)
    public_channel_id = channels.channels_create(user1['token'],"channel14",1)
    # error as start index is 0 but messages is empty as no msgs sent
    with pytest.raises(InputError):
        assert channel.channel_messages(user1['token'],public_channel_id['channel_id'],1)

def test_channel_messages_failure_wrong_input():
    # clearing data
    other.clear()
    # registering 2 users
    user1 = auth.auth_register('user17@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register('user27@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    # user 1 creates a channel
    public_channel_id = channels.channels_create(user1['token'],"channel17",1)
    with pytest.raises(InputError):
        # puts in invalid channel_id
        channel.channel_messages(user1['token'],25,0)
    with pytest.raises(InputError):
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
    with pytest.raises(AccessError):
        # user2 is not in the channel
        channel.channel_messages(user2['token'],public_channel_id['channel_id'],0)
    with pytest.raises(AccessError):
        # invalid token
        channel.channel_messages('faweebawoowaba' + user2['token'],public_channel_id['channel_id'],0)

# ===========================================================================================

# tests for when message_send() is implemented

def test_channel_messages_success_25_msgs():
    other.clear()
    user1 = auth.auth_register('user16@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user26@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    public_channel_id = channels.channels_create(user1['token'],"channel16",1)
    channel.channel_invite(user1['token'],public_channel_id['channel_id'],user2['u_id'])
    for i in range(25):
        message.message_send(user1['token'],public_channel_id['channel_id'],'testing123')
        public_channel_id['channel_id'] = public_channel_id['channel_id'] + i - i
    result = channel.channel_messages(user1['token'],public_channel_id['channel_id'],0)
    assert result['start'] == 0
    assert result['end'] == -1

def test_channel_messages_success_50_msgs():
    other.clear()
    user1 = auth.auth_register('user16@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user26@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    public_channel_id = channels.channels_create(user1['token'], "channel16", 1)
    channel.channel_invite(user1['token'], public_channel_id['channel_id'], user2['u_id'])
    for i in range(60):
        message.message_send(user1['token'], public_channel_id['channel_id'], 'testing123')
        public_channel_id['channel_id'] = public_channel_id['channel_id'] + i - i
    result = channel.channel_messages(user1['token'], public_channel_id['channel_id'], 5)
    assert result['start'] == 5
    assert result['end'] == 55

#tests for channel_leave

def test_channel_leave_input_error():
    #code for exception where Channel ID is not a valid channel
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    with pytest.raises(InputError):
        channel.channel_leave(user1['token'], -2) # Expect fail since channel-2 doesn't exist


def test_channel_leave_access_error():
#accessError when trying to remove user identified by 'token' from channel 1
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    #have to leave a channel twice to throw accesserror
    channel.channel_leave(user1['token'], new_channel_id['channel_id'])
    with pytest.raises(AccessError):
        #auth_user should no longer be in the channel
        channel.channel_leave(user1['token'], new_channel_id['channel_id'])


def test_channel_leave_success():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    #auth user becomes a member + owner, upon channel creation
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    channel.channel_leave(user1['token'], new_channel_id['channel_id'])
    joined_channels = channels.channels_list(user1['token'])
    assert joined_channels['channels'] == []


#tests for channel_join

def test_channel_join_input_error():
    #code for exception where Channel ID is not a valid channel
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    with pytest.raises(InputError):
        channel.channel_join(user1['token'], -2) # Expect fail since channel-2 doesn't exist

def test_channel_join_access_error():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'aaa123123', 'ree', 'Path')
    #private channel created by user1
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', False)
    #user2 attemps to join private channel
    with pytest.raises(AccessError):
        #expect to fail
        channel.channel_join(user2['token'], new_channel_id['channel_id'])


def test_channel_join_success_public():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'aaa123123', 'Aeere', 'Path')
    #private channel created by user2
    new_channel_id = channels.channels_create(user2['token'],'myEpicChannel', True)
    #user1 attemps to join public channel
    channel.channel_join(user1['token'], new_channel_id['channel_id'])
    user1_joined_channels = channels.channels_list(user1['token'])
    assert user1_joined_channels['channels'] == [
        {
            'channel_id': new_channel_id['channel_id'],
            'name' : 'myEpicChannel'
        }
    ]

def test_channel_join_success_private():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'aaa123123', 'ree', 'Path')
    #private channel created by user2
    new_channel_id = channels.channels_create(user2['token'],'myEpicChannel', False)
    #user1 attemps to join private channel, succeeds bc user1 is global owner
    channel.channel_join(user1['token'], new_channel_id['channel_id'])
    members_of_myEpicChannel = channel.channel_details(user1['token'], new_channel_id['channel_id'])
    assert members_of_myEpicChannel['all_members'] == [
        {
            'u_id': user2['u_id'],
            'name_first': 'ree',
            'name_last': 'Path',
            'profile_img_url': '',
        },
        {
            'u_id': user1['u_id'],
            'name_first': 'Shree',
            'name_last': 'Nath',
            'profile_img_url': '',
        }
    ]

#tests for channel_addowner

#code for exception where Channel ID is not a valid channel
def test_channel_addowner_input_error1():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'aaa123123', 'ree', 'Path')
    with pytest.raises(InputError):
        channel.channel_addowner(user1['token'], -2, user2['u_id']) # Expect fail since channel-2 doesn't exist

#trying to add an existing owner as an owner
def test_channel_addowner_input_error2():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    with pytest.raises(InputError):
        channel.channel_addowner(user1['token'], new_channel_id['channel_id'], user1['u_id'])

#accesserror when auth_user is not an owner of the channel
def test_channel_addowner_access_error_not_owner():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    user3 = auth.auth_register('haha3@gmail.com', 'Asdssdd23232', 'Aeeree', 'Bath')
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    #fail since user2 is not an owner of the created channel, nor a global user
    with pytest.raises(AccessError):
        channel.channel_addowner(user2['token'], new_channel_id['channel_id'], user3['u_id'])

def test_channel_addowner_access_error_not_global():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    user3 = auth.auth_register('haha3@gmail.com', 'Asdssdd23232', 'Aeeree', 'Bath')
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    #fail since user2 is not an owner of the created channel, nor a global user
    with pytest.raises(AccessError):
        channel.channel_addowner(user3['token'], new_channel_id['channel_id'], user2['u_id'])

def test_channel_addowner_global_owner_success():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    user3 = auth.auth_register('haha3@gmail.com', 'Asdssdd23232', 'Aeeree', 'Bath')
    new_channel_id = channels.channels_create(user2['token'],'myEpicChannel', True)
    #user1 can add user3 to the channel because user1 is a global owner
    channel.channel_invite(user2['token'],new_channel_id['channel_id'],user3['u_id'])
    channel.channel_addowner(user1['token'], new_channel_id['channel_id'], user3['u_id'])
    user3_joins_channel = channel.channel_details(user3['token'], new_channel_id['channel_id'])
    assert user3_joins_channel['owner_members'] == [
        {
            'u_id': user2['u_id'],
            'name_first': 'Aeep',
            'name_last': 'Path',
            'profile_img_url': '',
        },
        {
            'u_id': user3['u_id'],
            'name_first': 'Aeeree',
            'name_last': 'Bath',
            'profile_img_url': '',
        },
    ]

def test_channel_addowner_channel_owner_success():
    other.clear()
    auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    user3 = auth.auth_register('haha3@gmail.com', 'Asdssdd23232', 'Aeeree', 'Bath')
    new_channel_id = channels.channels_create(user2['token'],'myEpicChannel', True)
    #user2 can add user3 to the channel because user2 is channel owner
    channel.channel_addowner(user2['token'], new_channel_id['channel_id'], user3['u_id'])
    user3_joins_channel = channel.channel_details(user3['token'], new_channel_id['channel_id'])
    assert user3_joins_channel['owner_members'] == [
        {
            'u_id': user2['u_id'],
            'name_first': 'Aeep',
            'name_last': 'Path',
            'profile_img_url': '',
        },
        {
            'u_id': user3['u_id'],
            'name_first': 'Aeeree',
            'name_last': 'Bath',
            'profile_img_url': '',
        },
    ]

#tests for channel_removeowner

def test_channel_removeowner_InputError_invalid_channel():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    with pytest.raises(InputError):
        channel.channel_removeowner(user1['token'], -2, user1['u_id']) # Expect fail since channel-2 doesn't exist

def test_channel_removeowner_InputError_not_owner():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    #user1 creates channel
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    with pytest.raises(InputError):
        #input error when trying to remove user2 as an owner
        channel.channel_removeowner(user1['token'], new_channel_id['channel_id'], user2['u_id'])

def test_channel_removeowner_AccessError():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    #user1 creates channel
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    with pytest.raises(AccessError):
        #access error because user is not a global_owner, or a channel owner
        channel.channel_removeowner(user2['token'], new_channel_id['channel_id'], user1['u_id'])


def test_channel_removeowner_success_channel_owner():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    #user1 creates channel
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    channel.channel_addowner(user1['token'], new_channel_id['channel_id'], user2['u_id'])
    channel.channel_removeowner(user1['token'], new_channel_id['channel_id'], user2['u_id'])
    user1s_channel = channel.channel_details(user1['token'], new_channel_id['channel_id'])
    assert user1s_channel['owner_members'] == [
        {
            'u_id': user1['u_id'],
            'name_first': 'Shree',
            'name_last': 'Nath',
            'profile_img_url': '',
        }
    ]

def test_channel_removeowner_success_global_owner():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    user3 = auth.auth_register('haha3@gmail.com', 'Asdssdd23232', 'Aeeree', 'Bath')
    new_channel_id = channels.channels_create(user2['token'],'myEpicChannel', True)
    channel.channel_addowner(user2['token'], new_channel_id['channel_id'], user3['u_id'])
    channel.channel_removeowner(user1['token'], new_channel_id['channel_id'], user3['u_id'])
    user2s_channel = channel.channel_details(user2['token'], new_channel_id['channel_id'])
    assert user2s_channel['owner_members'] == [
        {
            'u_id': user2['u_id'],
            'name_first': 'Aeep',
            'name_last': 'Path',
            'profile_img_url': '',
        }
    ]

def test_invalid_tokens_for_channel_functions():
    other.clear()
    user1 = auth.auth_register('user12@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user22@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    user3 = auth.auth_register('userwabi@gmail.com', '123abc!@#', 'Richard', 'Dawkins')
    new_channel_id = channels.channels_create(user2['token'],'myEpicChannel', True)
    with pytest.raises(AccessError):
        #invalid tokens!
        channel.channel_leave('faweba' + user2['token'], new_channel_id['channel_id'])
    with pytest.raises(AccessError):
        channel.channel_join('faweba' + user1['token'], new_channel_id['channel_id'])
    with pytest.raises(AccessError):
        channel.channel_addowner('faweba' + user2['token'], new_channel_id['channel_id'], user3['u_id'])
    with pytest.raises(AccessError):
        channel.channel_removeowner('faweba' + user2['token'], new_channel_id['channel_id'], user2['u_id'])