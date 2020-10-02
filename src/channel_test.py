import channel
import pytest
import data
import error


#tests for channel_leave

def test_channel_leave_success():
    #add channel_create
    #inputs: token (me), ch_id, u_id
    channel.channel_join('token', 0)
    result = channels.channels_list('token')
    assert result = [
        {
            'id': 0,
            'name' : 'channel0',
        }
    ]
    #inputs: token, ch_id
    channel.channel_leave('token', 0) # Expect to work since we invited user#0 to channel#0
    assert result = [

    ]


def test_channel_leave_input_error():
    #code for exception where Channel ID is not a valid channel
    with pytest.raises(InputError) as e:
        channel.channel_leave('token', 9999) # Expect fail since channel9999 doesn't exist


def test_channel_leave_access_error():
    #code for exception where Authorised user is not a member of channel with channel_id
    #invite user0 joins channel0
    channel.channel_join('token', 0)
    #accessError when trying to remove user identified by 'token' from channel 1
    with pytest.raises(AccessError) as e:
        channel.channel_leave('token', 1) # Expect fail since user0 never joined channel1



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
    assert result = [
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
