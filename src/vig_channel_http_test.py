import requests
import json
import pytest
import re
import signal
import jwt
import data
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


def test_post_invite(url):
 
    # users 1 and 2
    user_1_data = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    user_2_data = {
        'email': 'test21@email.com',
        'password': 'password1234',
        'name_first': 'test2',
        'name_last': 'user2'
    }

    user_3_data = {
        'email': 'test231@email.com',
        'password': 'passwo24rd1234',
        'name_first': 'test3',
        'name_last': 'user3'
    }

    # register users
    r = requests.post(url + "/auth/register", json=user_1_data)
    user_1 = r.json()

    r = requests.post(url + "/auth/register", json=user_2_data)
    user_2 = r.json()

    r = requests.post(url + "/auth/register", json=user_3_data)
    user_3 = r.json()

    # create channel
    channel_data = {
        'token': user_1['token'],
        'name': 'channel1',
        'is_public': True,
    }
    r = requests.post(url + "/channels/create", json=channel_data)
    channel_id = r.json()
    
    # invite user
    inv_data = {
        'token': user_1['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': user_2['u_id'],
    }
    r = requests.post(url + "/channel/invite", json=inv_data)

    # new member should be able to invite user 3
    inv_data = {
        'token': user_2['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': user_3['u_id'],
    }
    r = requests.post(url + "/channel/invite", json=inv_data)


def test_get_details(url):

    # users 1 and 2
    user_1_data = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    # register users
    r = requests.post(url + "/auth/register", json=user_1_data)
    user_1 = r.json()

    # create channel
    channel_data = {
        'token': user_1['token'],
        'name': 'channel1',
        'is_public': True,
    }
    r = requests.post(url + "/channels/create", json=channel_data)
    channel_id = r.json()

    # get channel details
    data_in = {
        'token': user_1['token'],
        'channel_id': channel_id['channel_id'],
    }

    r = requests.get(url + "/channel/details", params=data_in)
    channel_details = r.json()

    assert channel_details == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'test',
                'name_last': 'user',
            },
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'test',
                'name_last': 'user',
            },
        ],
    }


def test_get_messages(url):

    # users 1
    user_1_data = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    # register users
    r = requests.post(url + "/auth/register", json=user_1_data)
    user_1 = r.json()

    # create channel
    channel_data = {
        'token': user_1['token'],
        'name': 'channel1',
        'is_public': True,
    }
    r = requests.post(url + "/channels/create", json=channel_data)
    channel_id = r.json()

    # sending message
    data_in = {
        'token': user_1['token'],
        'channel_id': channel_id['channel_id'],
        'message': 'werules',
    }
    r = requests.post(url + "/message/send", json=data_in)

    # getting messages
    data_in = {
        'token': user_1['token'],
        'channel_id': channel_id['channel_id'],
        'start': 0,
    }
    r = requests.get(url + "/channel/messages", params=data_in)
    messagesss = r.json()
    assert messagesss == 'werules'

def test_post_invite_errors(url):

    # users 1 and 2
    user_1_data = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    user_2_data = {
        'email': 'test21@email.com',
        'password': 'password1234',
        'name_first': 'test2',
        'name_last': 'user2'
    }

    user_3_data = {
        'email': 'test231@email.com',
        'password': 'passwo24rd1234',
        'name_first': 'test3',
        'name_last': 'user3'
    }

    # register users
    r = requests.post(url + "/auth/register", json=user_1_data)
    user_1 = r.json()

    r = requests.post(url + "/auth/register", json=user_2_data)
    user_2 = r.json()

    r = requests.post(url + "/auth/register", json=user_3_data)
    user_3 = r.json()

    # create channel
    channel_data = {
        'token': user_1['token'],
        'name': 'channel1',
        'is_public': True,
    }
    r = requests.post(url + "/channels/create", json=channel_data)
    channel_id = r.json()
    
    # invite user but invalid user
    inv_data = {
        'token': user_2['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': user_3['u_id'],
    }
    r = requests.post(url + "/channel/invite", json=inv_data)

    assert r.status_code == 400
