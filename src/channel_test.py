import channel
import pytest
import data
import error


#tests for channel_leave


def test_channel_leave_success():
    #inputs: token (me), ch_id, u_id
    channel.channel_join('token', 0)
    #inputs: token, ch_id
    channel.channel_leave('token', 0) # Expect to work since we invited user#0 to channel#0


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
    #user joins channel0
    channel.channel_join('token', 0)

def test_channel_join_input_error():
    pass

def test_channel_join_access_error():
    pass



#tests for channel_addowner
