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
    u_id, token = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    with pytest.raises(InputError) as e:
        assert channel.channel_leave(token, -2) # Expect fail since channel-2 doesn't exist


def test_channel_leave_access_error():
#accessError when trying to remove user identified by 'token' from channel 1
    other.clear():
    u_id, token = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    channel_id = channels.channels_create(token,'myEpicChannel', True)
    #have to leave a channel twice to throw accesserror
    channel.channel_leave(token, channel_id)
    with pytest.raises(AccessError) as e:
        #auth_user should no longer be in the channel
        assert channel.channel_leave(token, channel_id)


def test_channel_leave_success():
    other.clear():
    u_id, token = auth.auth_register('haha@gmail.com', 'Password123123', 'Shree', 'Nath')
    #auth user becomes a member + owner, upon channel creation
    channel_id = channels.channels_create(token,'myEpicChannel', True)
    channel.channel_leave(token, channel_id)
    joined_channels = channels_list(token)
    assert joined_channels['channels'] == []



#tests for channel_join

def test_channel_join_success():
    channel_id_1 = channels.channels_create('token', 'new_channel1', True)
    channel_id_2 = channels.channels_create('token', 'new_channel2', True)
    #user joins channel1 and channel2

    channel.channel_join('token', channel_id_1)
    channel.channel_join('token', channel_id_2)
    #assuming channels_list is working properly, result should be a dictionary
    #of channel0 and channel1, the channels that the user has joined
    result = channels.channels_list(token)
    assert result == [
        {
            'id': 1,
            'name' : 'channel1',
        },
        {
            'id': 2,
            'name' : 'channel2',
        },
    ]


def test_channel_join_input_error():
    #user attemps to join an invalid channel (doesn't exist)
    with pytest.raises(InputError) as e:
        channel.channel_join('token', -1) # Expect fail since -1 should not be a valid channel id


def test_channel_join_access_error():
    #create a private channel
    channel_id = channels.channels_create('token', 'generic_name', False)
    #user attemps to join a channel which is private && authorised user is not a global owner
    with pytest.raises(AccessError) as e:
        #error should be raised if channel with ch_id 1, is a private channel
        channel.channel_join('token', channel_id)



#tests for channel_addowner
def test_channel_addowner_success():
    #create a channel called 'new_channel'
    ch_id = channels.channels_create('token', 'new_channel', True)
    #add user7 as owner to this channel
    channel.channel_addowner('token', ch_id, 7)
    #auth user joins this channel for channel_details to be useful
    channel.channel_join('token', ch_id)
    name, owner_members, all_members = channel.channel_details('token', ch_id)

    #assert that user7 is a part of the owner_members
    for member in owner_members:
        new_owner_success = 7 in member.values()

    assert new_owner_success == True




def test_channel_addowner_input_error1():
    #channel687 has not been created, thus input error
    with pytest.raises(InputError) as e:
        channel.channel_addowner('token', 687,6)


def test_channel_addowner_input_error2():
    #create a channel with inputs token, channel_name, isPublic
    channel_id = channels.channels_create('token', 'new_channel', True)
    #add user7 as owner to this channel
    channel.channel_addowner('token', ch_id, 7)
    #trying to add user7 as an owner to the channel more than once
    with pytest.raises(InputError) as e:
        channel.channel_addowner('token', ch_id, 7)


def test_channel_addowner_access_error():
    channel_id = channels.channels_create('token', 'new_channel', True)
    #raise AccessError if auth user is either:
    #1. owner of the flockr
    #2. owner of the channel
    with pytest.raises(AccessError) as e:
        channel.channel_join('token', channel_id)



#tests for channel_removeowner
def test_channel_removeowner_success():
    pass

def test_channel_removeowner_InputError1():
    pass

def test_channel_removeowner_InputError2():
    pass

def test_channel_removeowner_AccessError():
    pass
