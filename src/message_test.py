import message
import channels
import channel
import auth
import datetime
import pytest
from other import clear 
from error import InputError, AccessError

def test_message_send(): 
    other.clear()
    user1 = auth.auth_register('test@mail.com', 'GoodLuckHackers123', 'Hazm', 'Spazm'
    test_channel_one = channels.channels_create(user1['token'], 'My Test Channel', True)
    user2 = auth.auth_register('another@mail.com', 'easypewpew9', 'Sam', 'Keating')
    channel.channel_join(user2['token', test_channel_one['channel_id'])
    message_id = message.message_send(user2['token', test_channel_one['channel_id'], 'Test Message Hello Boom Boom Pop Pop')
    message_time = datetime.datetime.now().timestamp()
    assert test_channel_one['messages'] == [{
        'message_id': message_id,
        'u_id': user2['u_id'],
        'message': 'Test Message Hello Boom Boom Pop Pop',
        'time_created': message_time
    }] 

def test_message_send_unauthorised(): 
    other.clear()
    user1 = auth.auth_register('testrestpest@mail.com', 'CatDog222', 'Kanye', 'West')
    test_channel_two = channels.channels_create(user1['token'], 'Shady Channel', True)
    user2 = auth.auth_register('howto@mail.com', 'qwerasdf', 'Conner', 'Walsh')
    with pytest.raises(AccessError):
        message.message_send(user2['token'], test_channel_two['channel_id'], 'LET ME IN THE CHANNEL!!!!!')

    #Cannot cover 'InputError' - Message is more than 1000 characters within black box test
    #It is too messy to declare a message string that is 1000+ characeters 

def test_message_remove(): 
    