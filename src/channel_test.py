import channel
import channels
import auth
import pytest
import data
import error
import other

#assume: each test starts with an empty data structure and populates it
#tests for channel_leave

def test_channel_leave_input_error():
    #code for exception where Channel ID is not a valid channel
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    with pytest.raises(InputError) as e:
        channel.channel_leave(user1['token'], -2) # Expect fail since channel-2 doesn't exist


def test_channel_leave_access_error():
#accessError when trying to remove user identified by 'token' from channel 1
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    #have to leave a channel twice to throw accesserror
    channel.channel_leave(user1['token'], new_channel_id['channel_id'])
    with pytest.raises(AccessError) as e:
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
    with pytest.raises(InputError) as e:
        channel.channel_join(user1['token'], -2) # Expect fail since channel-2 doesn't exist

def test_channel_join_access_error():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'aaa123123', 'ree', 'Path')
    #private channel created by user1
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', False)
    #user2 attemps to join private channel
    with pytest.raises(AccessError) as e:
        #expect to fail
        channel.channel_join(user2['token'], new_channel_id['channel_id'])


def test_channel_join_success_public():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'aaa123123', 'Aeere', 'Path')
    #private channel created by user1
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    #user2 attemps to join public channel
    channel.channel_join(user2['token'], new_channel_id['channel_id'])
    user2_joined_channels = channels.channels_list(user2['token'])
    assert user2_joined_channels['channels'] == [
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
        },
        {
            'u_id': user1['u_id'],
            'name_first': 'Shree',
            'name_last': 'Nath',
        }
    ]

#tests for channel_addowner

#code for exception where Channel ID is not a valid channel
def test_channel_addowner_input_error1():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'aaa123123', 'ree', 'Path')
    with pytest.raises(InputError) as e:
        channel.channel_addowner(user1['token'], -2, user2['u_id']) # Expect fail since channel-2 doesn't exist

#trying to add an existing owner as an owner
def test_channel_addowner_input_error2():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    with pytest.raises(InputError) as e:
        channel.channel_addowner(user1['token'], new_channel_id['channel_id'], user1['u_id'])

#accesserror when auth_user is not an owner of the channel
def test_channel_addowner_access_error_not_owner():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    user3 = auth.auth_register('haha3@gmail.com', 'Asdssdd23232', 'Aeeree', 'Bath')
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    #fail since user2 is not an owner of the created channel, nor a global user
    with pytest.raises(AccessError) as e:
        channel.channel_addowner(user2['token'], new_channel_id['channel_id'], user3['u_id'])

def test_channel_addowner_access_error_not_global():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    user3 = auth.auth_register('haha3@gmail.com', 'Asdssdd23232', 'Aeeree', 'Bath')
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    #fail since user2 is not an owner of the created channel, nor a global user
    with pytest.raises(AccessError) as e:
        channel.channel_addowner(user3['token'], new_channel_id['channel_id'], user2['u_id'])

def test_channel_addowner_global_owner_success():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    user3 = auth.auth_register('haha3@gmail.com', 'Asdssdd23232', 'Aeeree', 'Bath')
    new_channel_id = channels.channels_create(user2['token'],'myEpicChannel', True)
    #user1 can add user3 to the channel because user1 is a global owner
    channel.channel_addowner(user1['token'], new_channel_id['channel_id'], user3['u_id'])
    user3_joins_channel = channel.channel_details(user3['token'], new_channel_id['channel_id'])
    assert user3_joins_channel['owner_members'] == [
        {
            'u_id': user2['u_id'],
            'name_first': 'Aeep',
            'name_last': 'Path',
        },
        {
            'u_id': user3['u_id'],
            'name_first': 'Aeeree',
            'name_last': 'Bath',
        },
    ]

def test_channel_addowner_channel_owner_success():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
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
        },
        {
            'u_id': user3['u_id'],
            'name_first': 'Aeeree',
            'name_last': 'Bath',
        },
    ]

#tests for channel_removeowner

def test_channel_removeowner_InputError_invalid_channel():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    with pytest.raises(InputError) as e:
        channel.channel_removeowner(user1['token'], -2) # Expect fail since channel-2 doesn't exist

def test_channel_removeowner_InputError_not_owner():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    #user1 creates channel
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    with pytest.raises(InputError) as e:
        #input error when trying to remove user2 as an owner
        channel.channel_removeowner(user1['token'], new_channel_id['channel_id'], user2['u_id'])

def test_channel_removeowner_AccessError():
    other.clear()
    user1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    user2 = auth.auth_register('haha2@gmail.com', 'Aaa123123ffff', 'Aeep', 'Path')
    #user1 creates channel
    new_channel_id = channels.channels_create(user1['token'],'myEpicChannel', True)
    with pytest.raises(AccessError) as e:
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
        }
    ]
