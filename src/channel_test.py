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
    other.clear():
    register1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    with pytest.raises(InputError) as e:
        assert channel.channel_leave(register1['token'], -2) # Expect fail since channel-2 doesn't exist


def test_channel_leave_access_error():
#accessError when trying to remove user identified by 'token' from channel 1
    other.clear():
    register1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    channel_id = channels.channels_create(register1['token'],'myEpicChannel', True)
    #have to leave a channel twice to throw accesserror
    channel.channel_leave(register1['token'], channel_id['channel_id'])
    with pytest.raises(AccessError) as e:
        #auth_user should no longer be in the channel
        assert channel.channel_leave(token, channel_id['channel_id'])


def test_channel_leave_success():
    other.clear():
    register1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    #auth user becomes a member + owner, upon channel creation
    channel_id = channels.channels_create(register1['token'],'myEpicChannel', True)
    channel.channel_leave(register1['token'], channel_id['channel_id'])
    joined_channels = channels_list(register1['token'])
    assert joined_channels['channels'] == []


#tests for channel_join

def test_channel_join_input_error():
    #code for exception where Channel ID is not a valid channel
    other.clear():
    register1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    with pytest.raises(InputError) as e:
        assert channel.channel_join(register1['token'], -2) # Expect fail since channel-2 doesn't exist

def test_channel_join_access_error():
    other.clear():
    register1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    register2 = auth.auth_register('haha2@gmail.com', 'aaa123123', 'ree', 'Path')
    #private channel created by user1
    channel_id = channels.channels_create(register1['token'],'myEpicChannel', False)
    #user2 attemps to join private channel
    with pytest.raises(AccessError) as e:
        #auth_user should no longer be in the channel
        assert channel.channel_join(register2['token'], channel_id['channel_id'])


def test_channel_join_success():
    other.clear():
    register1 = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    register2 = auth.auth_register('haha2@gmail.com', 'aaa123123', 'Aee[]', 'Path')
    #private channel created by user1
    new_channel_id = channels.channels_create(register1['token'],'myEpicChannel', True)
    #user2 attemps to join public channel
    channel.channel_join(register2['token'], new_channel_id['channel_id'])
    user2_joined_channels = channels_list(register2['token'])
    assert user2_joined_channels['channels'] == [
        {
            'channel_id': new_channel_id['channel_id'],
            'name' : 'myEpicChannel'
        }
    ]


## TODO: 4/10/20 morning

#tests for channel_addowner
def test_channel_addowner_success():
    pass

def test_channel_addowner_input_error1():
    pass

def test_channel_addowner_input_error2():
    pass

def test_channel_addowner_access_error():
    pass



#tests for channel_removeowner
def test_channel_removeowner_success():
    pass

def test_channel_removeowner_InputError1():
    pass

def test_channel_removeowner_InputError2():
    pass

def test_channel_removeowner_AccessError():
    pass
