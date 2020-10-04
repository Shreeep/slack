import channels
import channel
import auth
import pytest 
from error import AccessError, InputError
import data
import other

#Testing if {user, token} is apart of channel - it should return the asscoiated channel 
def test_channels_list():
    user1 = auth.auth_register('poo@gmail.com', 'yep123', 'John', 'Smith')
    test_channel_one = channels.channels_create(user1['token'], 'Public Channel', True)
    channel_list = channels.channels_list(user1['token'])
    assert channel_list == {
        'channels': [
        	{
        		'channel_id': test_channel_one['channel_id'],
        		'name': 'Public Channel',
        	}
        ],
    }

#Testing if function returns empty list in case of a {user, token} not being apart of any channels 
def test_channels_list_empty(): 
    result = auth.auth_register('test@email.com', '123abc', 'Big', 'Chungus') 
    assert channels.channels_list(result['token']) == {'channels':[]}

#channels_listall should return both Public and Private channels associated with user1 and user2 
#Assuming return value will be the same for all tokens passed through since it is ALL channels 
def test_channels_listall():
    other.clear()
    user1 = auth.auth_register('testa@email.com', 'qwer123', 'Hugh', 'Mungus')
    user2 = auth.auth_register('testb@email.com', 'abc123', 'Hasm', 'Spasm')
    test_channel_two = channels.channels_create(user1['token'], 'User 1s Channel', True) #Public Channel
    test_channel_three = channels.channels_create(user2['token'], 'User 2s Channel', False) #Private Channel
    all_channels_list = channels.channels_listall(user1['token'])
    assert all_channels_list == {
        'channels':[
            {
                'channel_id': test_channel_two['channel_id'],
                'name': 'User 1s Channel',
            },

            {
                'channel_id': test_channel_three['channel_id'],
                'name': 'User 2s Channel',
            }
        ]
    }

#Two users with no channels
#Should return an empty list
def test_channels_listall_empty():
    other.clear()
    user1 = auth.auth_register('testc@email.com', 'qwdss34er', 'Bugh', 'Dungus')
    user2 = auth.auth_register('testd@email.com', 'abcqwe123', 'Sasm', 'Pasm')
    empty_channels = {'channels':[]}
    assert channels.channels_listall(user1['token']) == empty_channels and channels.channels_listall(user2['token']) == empty_channels

#Testing if creates a public channel
def test_channels_create_public():
    other.clear()
    user1 = auth.auth_register('teste@email.com', 'qweweerr', 'Jake', 'Johnson')
    public_channel = channels.channels_create(user1['token'], 'User1s Channel', True)
    user2 = auth.auth_register('testfun@gmail.com', '1235asd', 'Bob', 'Thebuilder')
    #If channel is public, user2 joins without error
    channel.channel_join(user2['token'], public_channel['channel_id'])

#Testing if creates a private channel
def test_channels_create_private():
    other.clear()
    user1 = auth.auth_register('testf@email.com', 'qsdf123', 'Matthew', 'Mughus')
    private_channel = channels.channels_create(user1['token'], 'User1s Channel', False)
    user2 = auth.auth_register('testfun@gmail.com', '1235asd', 'Bob', 'Thebuilder')
    with pytest.raises(AccessError) as e:
        channel.channel_join(user2['token'], private_channel['channel_id'])


#Input Error should be raised if channel name is more than 20 characters long i.e. len(channel_name) > 20
def test_channels_create_input_error():
    other.clear()
    user1 = auth.auth_register('teste@email.com', 'qsdasdf', 'Matthew', 'Mahogonny')
    with pytest.raises(InputError) as e:
        channels.channels_create(user1['token'], '123456789101213141516171819', True)

def test_invalid_tokens_for_channels_functions():
    other.clear()
    user1 = auth.auth_register('testc@email.com', 'qwdss34er', 'Bugh', 'Dungus')
    user2 = auth.auth_register('testd@email.com', 'abcqwe123', 'Sasm', 'Pasm')
    test_channel_one = channels.channels_create(user1['token'], 'Public Channel', True)
    with pytest.raises(AccessError) as e:
        channels.channels_list('faweeba' + user1['token'])
    with pytest.raises(AccessError) as e:
        channels.channels_listall('faweeba' + user1['token'])
    with pytest.raises(AccessError) as e:
        channels.channels_create('faweeba' + user1['token'], 'Public nuisance', True)





