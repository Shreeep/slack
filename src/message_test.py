import message
import channels
import channel
import auth
import pytest
import other
import data
from error import InputError, AccessError

#White Box: 
def test_message_send(): 
    other.clear()
    user1 = auth.auth_register('test@mail.com', 'GoodLuckHackers123', 'Hazm', 'Spazm')
    user2 = auth.auth_register('another@mail.com', 'easypewpew9', 'Sam', 'Keating')
    test_channel = channels.channels_create(user1['token'], 'Channel #1', True)
    channels.channels_create(user1['token'], 'Another Channel', True)
    channel.channel_join(user2['token'], test_channel['channel_id'])
    message_id = message.message_send(user2['token'], test_channel['channel_id'], 'Test Message Hello Boom Boom Pop Pop')
    assert data.data['channels'][0]['messages'][0] == {
        'message_id': message_id['message_id'],
        'u_id': user2['u_id'],
        'message': 'Test Message Hello Boom Boom Pop Pop',
        'time_created': data.data['channels'][0]['messages'][0]['time_created'],
    }

#Black Box: 
def test_message_send_unauthorised():
    other.clear()
    user1 = auth.auth_register('testrestpest@mail.com', 'CatDog222', 'Kanye', 'West')
    user2 = auth.auth_register('howto@mail.com', 'qwerasdf', 'Conner', 'Walsh')
    test_channel_two = channels.channels_create(user1['token'], 'Shady Channel', True)
    channels.channels_create(user1['token'], 'Another Channel', True)
    with pytest.raises(AccessError):
        message.message_send(user2['token'], test_channel_two['channel_id'], 'LET ME IN THE CHANNEL!')

def test_message_remove(): 
    other.clear()
    user1 = auth.auth_register('bruce@gmail.com', 'bombim123', 'Bruce', 'Lee')
    test_channel_three = channels.channels_create(user1['token'], 'test channel', True)
    channels.channels_create(user1['token'], 'Another Channel', True)
    user_message = message.message_send(user1['token'], test_channel_three['channel_id'], 'test message')
    message.message_remove(user1['token'], user_message['message_id'])
    

def test_message_remove_no_longer_exists(): 
    other.clear()
    user1 = auth.auth_register('bigbob123@mail.com', 'CatDog222', 'John', 'Shepard')
    test_channel_four = channels.channels_create(user1['token'], 'QWER Channel', True)
    channels.channels_create(user1['token'], 'Another Channel', True)
    message_id = message.message_send(user1['token'], test_channel_four['channel_id'], 'Hey How are u? oops i didnt mean to send that let me remove it')
    message.message_remove(user1['token'], message_id['message_id'])
    #Raise Input Error if the function is called again - since the message will not exist
    with pytest.raises(InputError):
        message.message_remove(user1['token'], message_id['message_id'])

def test_message_remove_unauthorised(): 
    other.clear()
    user1 = auth.auth_register('testrestpest@mail.com', 'Cagqaw2', 'Kanye', 'West')
    test_channel_five = channels.channels_create(user1['token'], 'Shady Channel', True)
    channels.channels_create(user1['token'], 'Another Channel', True)
    user2 = auth.auth_register('howto@mail.com', 'qwerasdf', 'Conner', 'Walsh')
    message_id = message.message_send(user1['token'], test_channel_five['channel_id'], 'Hi User2, try remove this message, i dare u')
    #Access Error raised if user2 (who is only a member) - tries to remove the user1's (owner) message
    with pytest.raises(AccessError):
        message.message_remove(user2['token'], message_id['message_id'])

def test_message_remove_owner_permission():
    other.clear()
    user1_owner = auth.auth_register('rando@mail.com', '123avsad', 'John', 'Smith')
    test_channel = channels.channels_create(user1_owner['token'], 'Channel #9000', True)
    channels.channels_create(user1_owner['token'], 'Another Channel', True)
    user2_member = auth.auth_register('howto@mail.com', 'qwerasdf', 'Conner', 'Walsh')
    channel.channel_join(user2_member['token'], test_channel['channel_id'])
    message_id = message.message_send(user2_member['token'], test_channel['channel_id'], 'Testing if owner can remove my message')
    message.message_remove(user1_owner['token'], message_id['message_id'])

def test_message_edit(): 
    other.clear()
    user1 = auth.auth_register('tyuit@mail.com', '4234safs2', 'Joe', 'Rogan')
    test_channel_six = channels.channels_create(user1['token'], 'Channel #6', True)
    channels.channels_create(user1['token'], 'Another Channel', True)
    message_id = message.message_send(user1['token'], test_channel_six['channel_id'], 'Correct the spooling')
    message.message_edit(user1['token'], message_id['message_id'], 'Correct the spelling')
    

def test_message_edit_unauthorised():
    other.clear()
    user1 = auth.auth_register('yahooo@mail.com', 'Cagqaw2', 'Bing', 'Bong')
    test_channel_seven = channels.channels_create(user1['token'], 'Channel #7', True)
    channels.channels_create(user1['token'], 'Another Channel', True)
    user2 = auth.auth_register('megao@mail.com', 'qwerasdf', 'Lol', 'Peterson')
    message_id = message.message_send(user1['token'], test_channel_seven['channel_id'], 'Try and edit this message user2')
    with pytest.raises(AccessError):
        message.message_edit(user2['token'], message_id['message_id'], 'I cant edit your message user1, I am only a member')

def test_message_edit_owner_permission():
    other.clear()
    user1_owner = auth.auth_register('rando@mail.com', '123avsad', 'John', 'Smith')
    test_channel = channels.channels_create(user1_owner['token'], 'Channel #9000', True)
    channels.channels_create(user1_owner['token'], 'Another Channel', True)
    user2_member = auth.auth_register('howto@mail.com', 'qwerasdf', 'Conner', 'Walsh')
    channel.channel_join(user2_member['token'], test_channel['channel_id'])
    message_id = message.message_send(user2_member['token'], test_channel['channel_id'], 'Testing if owner can edit my message')
    message.message_edit(user1_owner['token'], message_id['message_id'], 'Yes Buddy, I Can edit your messages')

def test_message_edit_user_permission(): 
    other.clear()
    user1_owner = auth.auth_register('rando@mail.com', '123avsad', 'John', 'Smith')
    test_channel = channels.channels_create(user1_owner['token'], 'Channel #9000', True)
    channels.channels_create(user1_owner['token'], 'Another Channel', True)
    user2_member = auth.auth_register('howto@mail.com', 'qwerasdf', 'Conner', 'Walsh')
    channel.channel_join(user2_member['token'], test_channel['channel_id'])
    message_id = message.message_send(user2_member['token'], test_channel['channel_id'], 'Testing if I can edit my own message')
    message.message_edit(user2_member['token'], message_id['message_id'], 'Yay - I can edit my own messages..duhh im a member')

def test_message_edit_empty():
    other.clear()
    user1 = auth.auth_register('qwertyuwer@mail.com', '123abcasd', 'Jack', 'Ripper')
    test_channel = channels.channels_create(user1['token'], 'Test Channel B', True)
    channels.channels_create(user1['token'], 'Another Channel', True)
    message_id = message.message_send(user1['token'], test_channel['channel_id'], 'Random Message String asdasdsadas')
    message.message_edit(user1['token'], message_id['message_id'], '')

