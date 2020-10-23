import message
import channels
import channel
import auth
import datetime
import pytest
import other
import other 
from error import InputError, AccessError

def test_message_send(): 
    other.clear()
    user1 = auth.auth_register('test@mail.com', 'GoodLuckHackers123', 'Hazm', 'Spazm')
    user2 = auth.auth_register('another@mail.com', 'easypewpew9', 'Sam', 'Keating')
    test_channel = channels.channels_create(user1['token'], 'Channel #1', True)
    channel.channel_join(user2['token'], test_channel['channel_id'])
    message.message_send(user2['token'], test_channel['channel_id'], 'Test Message Hello Boom Boom Pop Pop')
    datetime.datetime.now().timestamp()

def test_message_send_unauthorised():
    other.clear()
    user1 = auth.auth_register('testrestpest@mail.com', 'CatDog222', 'Kanye', 'West')
    user2 = auth.auth_register('howto@mail.com', 'qwerasdf', 'Conner', 'Walsh')
    test_channel_two = channels.channels_create(user1['token'], 'Shady Channel', True)
    with pytest.raises(AccessError):
        message.message_send(user2['token'], test_channel_two['channel_id'], 'LET ME IN THE CHANNEL!')

def test_message_remove(): 
    other.clear()
    user1 = auth.auth_register('testrestpest@mail.com', 'CatDog222', 'Kanye', 'West')
    test_channel_three = channels.channels_create(user1['token'], 'Shady Channel', True)
    message_id = message.message_send(user1['token'], test_channel_three['channel_id'], 'Hey How are u? oops i didnt mean to send that let me remove it')
    message.message_remove(user1['token'], message_id)
    

def test_message_remove_no_longer_exists(): 
    other.clear()
    user1 = auth.auth_register('GIGA@mail.com', 'CatDog222', 'Lebron', 'James')
    test_channel_four = channels.channels_create(user1['token'], 'QWER Channel', True)
    message_id = message.message_send(user1['token'], test_channel_four['channel_id'], 'Hey How are u? oops i didnt mean to send that let me remove it')
    message.message_remove(user1['token'], message_id)
    #Raise Input Error if the function is called again - since the message will not exist
    with pytest.raises(InputError):
        message.message_remove(user1['token'], message_id)

def test_message_remove_unauthorised(): 
    other.clear()
    user1 = auth.auth_register('testrestpest@mail.com', 'Cagqaw2', 'Kanye', 'West')
    test_channel_five = channels.channels_create(user1['token'], 'Shady Channel', True)
    user2 = auth.auth_register('howto@mail.com', 'qwerasdf', 'Conner', 'Walsh')
    message_id = message.message_send(user1['token'], test_channel_five['channel_id'], 'Hi User2, try remove this message, i dare u')
    #Access Error raised if user2 (who is only a member) - tries to remove the user1's (owner) message
    with pytest.raises(AccessError):
        message.message_remove(user2['token'], message_id)

def test_message_remove_owner_permission():
    other.clear()
    user1_owner = auth.auth_register('rando@mail.com', '123avsad', 'John', 'Smith')
    test_channel = channels.channels_create(user1_owner['token'], 'Channel #9000', True)
    user2_member = auth.auth_register('howto@mail.com', 'qwerasdf', 'Conner', 'Walsh')
    channel.channel_join(user2_member['token'], test_channel['channel_id'])
    message_id = message.message_send(user2['token'], test_channel['channel_id'], 'Testing if owner can remove my message')
    message.message_remove(user1_owner['token'], message_id)
    assert test_channel['messages'] == []

def test_message_edit(): 
    other.clear()
    user1 = auth.auth_register('tyuit@mail.com', '4234safs2', 'Joe', 'Rogan')
    test_channel_six = channels.channels_create(user1['token'], 'Channel #6', True)
    message_id = message.message_send(user1['token'], test_channel_six['channel_id'], 'Correct the spooling')
    message.message_edit(user1['token'], message_id, 'Correct the spelling')
    message_time = datetime.datetime.now().timestamp()
    assert test_channel_six['messages'] == [{
        'message_id': message_id,
        'u_id': user1['u_id'],
        'message': 'Correct the spelling',
        'time_created': message_time
    }] 

def test_message_edit_unauthorised():
    other.clear()
    user1 = auth.auth_register('yahooo@mail.com', 'Cagqaw2', 'Bing', 'Bong')
    test_channel_seven = channels.channels_create(user1['token'], 'Channel #7', True)
    user2 = auth.auth_register('megao@mail.com', 'qwerasdf', 'Lol', 'Peterson')
    message_id = message.message_send(user1['token'], test_channel_seven['channel_id'], 'Try and edit this message user2')
    with pytest.raises(AccessError):
        message_edit(user2['token'], message_id, 'I cant edit your message user1, I am only a member')

def test_message_edit_owner_permission():
    other.clear()
    user1_owner = auth.auth_register('rando@mail.com', '123avsad', 'John', 'Smith')
    test_channel = channels.channels_create(user1_owner['token'], 'Channel #9000', True)
    user2_member = auth.auth_register('howto@mail.com', 'qwerasdf', 'Conner', 'Walsh')
    channel.channel_join(user2_member['token'], test_channel['channel_id'])
    message_id = message.message_send(user2_member['token'], test_channel['channel_id'], 'Testing if owner can edit my message')
    message.message_edit(user1_owner['token'], message_id, 'Yes Buddy, I Can edit your messages')
    message_time = datetime.datetime.now().timestamp()
    assert test_channel['messages'] == [{
        'message_id': message_id,
        'u_id': user2_member['u_id'],
        'message': 'Yes Buddy, I Can edit your messages',
        'time_created': message_time
    }] 

    
 