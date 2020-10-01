import channels
import channel
import pytest 
import error 

#Notes: 
    #channels_list is a subset of channels_listall
    #channels_list and channels_listall return a list of dictionaries, where each dictionary contains {channel_id, name}
    #Test Cases for channels_list(): 
        #User is apart of a channel - returns that channel 
        #No channels the user is apart of - returns an empty list 
        #User is apart of all channels - returns list of all channels 
        #User is apart of some channels, not all - returns list which is subset of all channels 
    #Test Cases for channels_listall():
        #No channels asscociated with the token - returns empty list
    #Test Cases for channels_create(): 
        #Channel name alredy exists 
        #Channel name is above 20 characters 

def test_channels_list():
    test_channel_one = channels.channels_create('random token', 'Channel #1', True)
    channel.channel_join('random token', test_channel_one) #does the token tell us which user to join the channel?? 
    result = channels.channels_list('random token')
    assert result == {
        'channels': [
        	{
        		'channel_id': test_channel_one,
        		'name': 'Channel #1',
        	}
        ],
    }

def test_channels_list_empty(): 
    assert channels.channels_list('token') == {}

def test_channels_listall():
    assert channels.channels_listall() == 

def test_channels_listall_empty():
    assert == {}

def test_channels_create_public():
    new_channel = channels.channels_create('token', 'My Channel', True)
    assert new_channel == ch_id
def test_channels_create_private():

def test_channels_create_already_exists():