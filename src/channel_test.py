import channel
import pytest
import data
import error


#tests for channel_leave

def test_channel_leave_success():
    #inputs: token (me), ch_id, u_id
    channel.channel_join('token', 0)
    result = channels.channels_list(token)
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
    #user joins channel1 and channel2
    channel.channel_join('token', 1)
    channel.channel_join('token', 2)
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
        channel.channel_join('token', 9999) # Expect fail since channel9999 was never created


def test_channel_join_access_error():
    channel_id = channels.channels_create('token', 'generic_name', False)
    #user attemps to join a channel which is private && authorised user is not a global owner
    with pytest.raises(AccessError) as e:
        #error should be raised if channel with ch_id 1, is a private channel
        channel.channel_join('token', channel_id) # Expect fail since user0 never joined channel1



#tests for channel_addowner
