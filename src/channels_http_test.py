import json
import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests

@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_get_channels_list(url):

    # User info:
    user1 = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }
    # Register user:
    register_user1 = requests.post(url + "/auth/register", json=user1)
    payload_user1 = register_user1.json()

    #Create channel associated with user:
    test_channel_one_details = {
        'token': payload_user1['token'],
        'name': 'Public Channel #1',
        'is_public': True
    }
    create_channel_one = requests.post(url + "/channels/create", json=test_channel_one_details)
    payload_channel_one = create_channel_one.json()
    
    #Create a second channel associated with user:
    test_channel_two_details = {
        'token': payload_user1['token'],
        'name': 'Public Channel #2',
        'is_public': True
    }
    create_channel_two = requests.post(url + "/channels/create", json=test_channel_two_details)
    payload_channel_two = create_channel_two.json()
    
    # Get request the channel list for user 1
    channel_list_user1 = requests.get(url + "/channels/list", params={'token':payload_user1['token']})
    result = channel_list_user1.json()
    assert result == {
        'channels':[
            {
                'channel_id': payload_channel_one['channel_id'],
                'name': 'Public Channel #1',
            },
            {
                'channel_id': payload_channel_two['channel_id'],
                'name': 'Public Channel #2',
            },
        ]
    }

def test_get_channels_list_empty(url):

    # User info:
    user1 = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }
    # Register user:
    register_user1 = requests.post(url + "/auth/register", json=user1)
    payload_user1 = register_user1.json()

    # Get list of channels associated with user1
    channel_list_user1 = requests.get(url + "/channels/list", params={'token':payload_user1['token']})
    result = channel_list_user1.json()
    
    assert result == {
        'channels':[]
    }


def test_get_channels_listall(url):
    # User info:
    user1 = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }
    # Register user:
    register_user1 = requests.post(url + "/auth/register", json=user1)
    payload_user1 = register_user1.json()

    # Register a second user:
    # User info:
    user2 = {
        'email': 'another@email.com',
        'password': 'qwerty123',
        'name_first': 'bob',
        'name_last': 'builder'
    }
    # Register user:
    register_user2 = requests.post(url + "/auth/register", json=user2)
    payload_user2 = register_user2.json()

    # Each user makes their own channel: 

    test_channel_one_details = {
        'token': payload_user1['token'],
        'name': 'User 1''s Channel',
        'is_public': True
    }
    create_channel_one = requests.post(url + "/channels/create", json=test_channel_one_details)
    payload_channel_one = create_channel_one.json()

    test_channel_two_details = {
        'token': payload_user2['token'],
        'name': 'User 2''s Channel',
        'is_public': True
    }
    create_channel_two = requests.post(url + "/channels/create", json=test_channel_two_details)
    payload_channel_two = create_channel_two.json()

    all_channels_list = requests.get(url + "/channels/listall", params={'token':payload_user1['token']})
    result = all_channels_list.json()

    assert result == {
        'channels':[
            {
                'channel_id': payload_channel_one['channel_id'],
                'name': 'User 1s Channel',
            },

            {
                'channel_id': payload_channel_two['channel_id'],
                'name': 'User 2s Channel',
            }
        ]
    }

def test_get_channels_list_and_listall_invalid_user(url): 
    # User info:
    user1 = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    # Register user:
    register_user1 = requests.post(url + "/auth/register", json=user1)
    payload_user1 = register_user1.json()

    # Create channel associated with user
    test_channel_one_details = {
        'token': payload_user1['token'],
        'name': 'Public Channel #1',
        'is_public': True
    }
    # Unauthorised user: 
    user2 = {
        'email': 'qwer@email.com',
        'password': 'passworqwerd123',
        'name_first': 'jims',
        'name_last': 'mowing'
    }
    register_user2 = requests.post(url + "/auth/register", json=user2)
    payload_user2 = register_user2.json()

    create_channel_one = requests.post(url + "/channels/create", json=test_channel_one_details)
    payload_channel_one = create_channel_one.json()
    # If an invalid token requests a list or listall (that normally contains test_channel_one details)
    # Raise Access Error
    r_1 = requests.get(url + "/channels/list", params={'token': payload_user2['token']})
    r1_payload = r_1.json()
    r_2 = requests.get(url + "/channels/listall", params={'token': payload_user2['token']})
    r2_payload = r_2.json()
    assert r1_payload['channels'] == []
    assert r2_payload['channels'] ==  [
        {
            'channel_id': payload_channel_one['channel_id'],
            'name': 'Public Channel #1'
        }
    ]

def test_post_channels_create(url): 

    # User info:
    user1 = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }
    # Register user:
    register_user1 = requests.post(url + "/auth/register", json=user1)
    payload_user1 = register_user1.json()

    #Create channel associated with user:
    test_channel_one_details = {
        'token': payload_user1['token'],
        'name': 'Public Channel #1',
        'is_public': False
    }
    create_channel_one = requests.post(url + "/channels/create", json=test_channel_one_details)
    payload_channel_one = create_channel_one.json()
    assert payload_channel_one == {
        'channel_id': payload_channel_one['channel_id']
    }
    

def test_post_channel_create_name_too_long(url): 
    # User info:
    user1 = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }
    # Register user:
    register_user1 = requests.post(url + "/auth/register", json=user1)
    payload_user1 = register_user1.json()

    #Create channel associated with user:
    test_channel_one_details = {
        'token': payload_user1['token'],
        'name': '123456789101213141516171819',
        'is_public': False
    }
    r = requests.post(url + "/channels/create", json=test_channel_one_details)
    assert r.status_code == 400
