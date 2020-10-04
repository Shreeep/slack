import channels
import channel
import auth
import pytest 
import error 
import data

#Testing if {user, token} is apart of channel - it should return the asscoiated channel 
def test_channels_list():
    test_channel_one = channels.channels_create('random token', 'Public Channel', True)
    assert channels.channels_list('random token') == {
        'channels': [
        	{
        		'channel_id': test_channel_one,
        		'name': 'Public Channel',
        	}
        ],
    }

#Testing if function returns empty list in case of a {user, token} not being apart of any channels 
def test_channels_list_empty(): 
    result = auth.auth_register('test@email.com', '123abc', 'Big', 'Chungus') 
    assert channels.channels_list(result['token']) == {}

#channels_listall should return both Public and Private channels associated with user1 and user2 
#Assuming return value will be the same for all tokens passed through since it is ALL channels 
def test_channels_listall():
    user1 = auth.auth_register('testa@email.com', 'qwer', 'Hugh', 'Mungus')
    user2 = auth.auth_register('testb@email.com', 'abc123', 'Hasm', 'Spasm')
    channels.channels_create(user1['token'], 'User 1s Channel', True) #Public Channel
    channels.channels_create(user2['token'], 'User 2s Channel', False) #Private Channel
    assert channels.channels_listall(user1['token']) == data.data['channels'] 

#Two users with no channels
#Should return an empty list
def test_channels_listall_empty():
    user1 = auth.auth_register('testc@email.com', 'qwdss34er', 'Bugh', 'Dungus')
    user2 = auth.auth_register('testd@email.com', 'abcqwe123', 'Sasm', 'Pasm')
    assert channels.channels_listall(user1['token']) == {} and channels.channels_listall(user2['token']) == {}

#Testing if creates a public channel
def test_channels_create_public():
    user1 = auth.auth_register('teste@email.com', 'qweweerr', 'Jake', 'Johnson')
    public_channel = channels.channels_create(user1['token'], 'User1s Channel', True)
    assert public_channel == data.data['channels']['id'] and data.data['channels']['is_public'] == True

#Testing if creates a private channel
def test_channels_create_private():
    user1 = auth.auth_register('testf@email.com', 'qsdf', 'Matthew', 'Mughus')
    public_channel = channels.channels_create(user1['token'], 'User1s Channel', False)
    assert public_channel == data.data['channels']['id'] and data.data['channels']['is_public'] == False


#Input Error should be raised if channel name is more than 20 characters long i.e. len(channel_name) > 20
def test_channels_create_input_error():
    user1 = auth.auth_register('teste@email.com', 'qsdasdf', 'Matthew', 'Mahogonny')
    public_channel = channels.channels_create(user1['token'], '123456789101213141516171819', True)
    with pytest.raises(InputError) as e:
        assert len(data.data['channels']['name']) <= 20






