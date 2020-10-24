import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json

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
    pythonic_result = {
        'channels':[
            {
                'channel_id': payload_channel_one['channel_id'],
                'name': 'Public Channel #1',
            },
        ]
    }
    assert result == pythonic_result.json()

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

    # 
    channel_list_user1 = requests.get(url + "/channels/list", params={'token':payload_user1['token']})
    result = channel_list_user1.json()
    pythonic_result = {
        'channels':[]
    }
    assert result == pythonic_result.json()


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

    pythonic_result = {
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
    assert result == pythonic_result.json()

def test_get_channels_list_and_listall_invalid_user(): 
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
    create_channel_one = requests.post(url + "/channels/create", json=test_channel_one_details)
    payload_channel_one = create_channel_one.json()
    # If an invalid token requests a list or listall (that normally contains test_channel_one details)
    # Raise Access Error 
    with pytest.raises(AccessError):
        channel_list_user1 = requests.get(url + "/channels/list", params={'token': 'invalid' + payload_user1['token']})
    with pytest.raises(AccessError): 
        channel_list_user1 = requests.get(url + "/channels/listall", params={'token': 'invalid' + payload_user1['token']})

def test_post_channels_create(url): 

