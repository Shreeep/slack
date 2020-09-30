import channels
import pytest 
import error 

#Assumptions for channels_* functions: 
    #
data = {
    'users': [
        {
            'id': 1,
            'name' : 'user1',
        },
        {
            'id': 2,
            'name' : 'user2',
        },
    ],
    'channels': [
        {
            'id': 1,
            'name' : 'channel1',
        },
        {
            'id': 2,
            'name' : 'channel2',
        },
    ],
}

def test_channels_list():
    assert channels.channels_list() == # Data from global variable or data.py??

def test_channels_listall():
    assert channels.channels_listall() == ##
def test_channels_create():
    # Test will need an exception - will read up on exceptions and write test


