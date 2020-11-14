import requests
import json
import pytest
import re
import signal
import jwt
from subprocess import Popen, PIPE
from time import sleep

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

def test_post_standup_start(url):
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
    standup_start_info = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['channel_id'],
        'length': 3
    }
    result = requests.post(url + "/standup/start", json=standup_start_info)
    assert result.status_code == 200
    result = requests.post(url + "/standup/start", json=standup_start_info)
    assert result.status_code == 400

def test_post_standup_send(url):
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
    standup_start_info = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['channel_id'],
        'length': 3
    }
    result = requests.post(url + "/standup/start", json=standup_start_info)
    assert result.status_code == 200
    standup_send_info = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['channel_id'],
        'message': "hi",
    }
    result = requests.post(url + "/standup/send", json=standup_send_info)
    assert result.status_code == 200
    sleep(3)
    result = requests.post(url + "/standup/send", json=standup_send_info)
    assert result.status_code == 400

def test_get_standup_active(url):
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
    standup_start_info = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['channel_id'],
        'length': 3
    }
    result = requests.post(url + "/standup/start", json=standup_start_info)
    assert result.status_code == 200

    data_in = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['channel_id'],
    }

    result = requests.get(url + "/standup/active", params=data_in)
    payload = result.json()
    assert result.status_code == 200
    assert payload['is_active']
    data_in['channel_id'] += 10
    result = requests.get(url + "/standup/active", params=data_in)
    assert result.status_code == 400