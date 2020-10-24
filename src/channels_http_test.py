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
            {
                'channel_id': payload_channel_two['channel_id'],
                'name': 'Public Channel #2',
            }
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



def test_post_channels_create(url): 