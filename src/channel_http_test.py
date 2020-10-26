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

def test_post_channel_leave(url):
    #tests if channel_leave works

    # user info
    user1 = {
        'email': 'crazyfrog@email.com',
        'password': 'dingding321321',
        'name_first': 'crazy',
        'name_last': 'frog'
    }

    # register user
    register_user1 = requests.post(url + "/auth/register", json=user1)
    encoded_jwt_user1 = register_user1.json()

    channel1 = {
        'token' : encoded_jwt_user1['token'],
        'name' : 'CrazyFrogsNewChannel',
        'is_public' : True
    }

    #create channel
    create_channel_one = requests.post(url + "/channels/create", json=channel1)
    channel_one = create_channel_one.json()

    #assert that user1 is part of channel1
    user_list = requests.get(url + "/channels/list", params={'token':encoded_jwt_user1['token']})
    user1_channels = user_list.json()

    assert user1_channels['channels'] == [
        {
            'channel_id' : 1,
            'name' : "CrazyFrogsNewChannel"
        }
    ]

#PROBLEM CODE
    #leave channel inputs
    u1_leave_ch1_data = {
        'token' : encoded_jwt_user1['token'],
        'channel_id' : channel_one['channel_id']
    }
    #user 1 leaves channel 1
    requests.post(url + "/channel/leave", json=u1_leave_ch1_data)
#PROBLEM CODE

    #assert that user1 is no longer part of channel1 (or any channels)
    user_list = requests.get(url + "/channels/list", params={'token':encoded_jwt_user1['token']})
    user1_channels = user_list.json()

    assert user1_channels == {'channels' : []}


def test_post_channel_join(url):
    #tests if channel_leave works

    # user info
    user1 = {
        'email': 'crazyfrog@email.com',
        'password': 'dingding321321',
        'name_first': 'crazy',
        'name_last': 'frog'
    }

    # register user1
    register_user1 = requests.post(url + "/auth/register", json=user1)
    encoded_jwt_user1 = register_user1.json()

    # user info
    user2 = {
        'email': 'bigchungus@email.com',
        'password': 'raspberrypi321321',
        'name_first': 'bugs',
        'name_last': 'bunny'
    }

    # register user2
    register_user2 = requests.post(url + "/auth/register", json=user2)
    encoded_jwt_user2 = register_user2.json()


    channel1 = {
        'token' : encoded_jwt_user1['token'],
        'name' : 'CrazyFrogsNewChannel',
        'is_public' : True
    }

    #user1 creates channel
    create_channel_1 = requests.post(url + "/channels/create", json=channel1)
    encoded_channel_1 = create_channel_1.json()

    #channel join inputs
    u2_join_ch1_data = {
        'token' : encoded_jwt_user2['token'],
        'channel_id' : encoded_channel_1['channel_id']
    }
    #user 2 joins channel 1
    requests.post(url + "channel/join", json=u2_join_ch1_data)
    
    #assert that user2 is part of channel1
    user_list_2 = requests.get(url + "channels/list", params={'token':encoded_jwt_user2['token']})
    user2_channels = user_list_2.json()

    assert user2_channels == {'channels' : [
        {
            'channel_id': encoded_channel_1['channel_id'],
            'name' : 'CrazyFrogsNewChannel'
        }
    ]}
  

def test_post_channel_addowner(url):
    user1 = {
        'email': 'crazyfrog@email.com',
        'password': 'dingding321321',
        'name_first': 'crazy',
        'name_last': 'frog'
    }

    # register user1
    register_user1 = requests.post(url + "/auth/register", json=user1)
    encoded_jwt_user1 = register_user1.json()

    # user info
    user2 = {
        'email': 'bigchungus@email.com',
        'password': 'raspberrypi321321',
        'name_first': 'bugs',
        'name_last': 'bunny'
    }

    # register user2
    register_user2 = requests.post(url + "/auth/register", json=user2)
    encoded_jwt_user2 = register_user2.json()


    channel1 = {
        'token' : encoded_jwt_user1['token'],
        'name' : 'CrazyFrogsNewChannel',
        'is_public' : True
    }

    #user1 creates channel
    create_channel_1 = requests.post(url + "/channels/create", json=channel1)
    encoded_channel_1 = create_channel_1.json()

    addOwnerData = {
        'token' : encoded_jwt_user1['token'],
        'channel_id' : encoded_channel_1['channel_id'],
        'u_id' : encoded_jwt_user2['u_id']
    }


    #user1 adds user2 as an owner to the channel
    requests.post(url + "/channel/addowner", json=addOwnerData)

    #assert that user2 is part of channel1
    user_list_2 = requests.get(url + "channels/list", params={'token':encoded_jwt_user2['token']})
    user2_channels = user_list_2.json()
    
    assert user2_channels == {'channels' : [
        {
            'channel_id': encoded_channel_1['channel_id'],
            'name' : 'CrazyFrogsNewChannel'
        }
    ]}

def test_post_channel_removeowner(url):
    user1 = {
        'email': 'crazyfrog@email.com',
        'password': 'dingding321321',
        'name_first': 'crazy',
        'name_last': 'frog'
    }

    # register user1
    register_user1 = requests.post(url + "/auth/register", json=user1)
    encoded_jwt_user1 = register_user1.json()

    # user info
    user2 = {
        'email': 'bigchungus@email.com',
        'password': 'raspberrypi321321',
        'name_first': 'bugs',
        'name_last': 'bunny'
    }

    # register user2
    register_user2 = requests.post(url + "/auth/register", json=user2)
    encoded_jwt_user2 = register_user2.json()


    channel1 = {
        'token' : encoded_jwt_user1['token'],
        'name' : 'CrazyFrogsNewChannel',
        'is_public' : True
    }

    #user1 creates channel
    create_channel_1 = requests.post(url + "/channels/create", json=channel1)
    encoded_channel_1 = create_channel_1.json()

    addRemoveOwnerData = {
        'token' : encoded_jwt_user1['token'],
        'channel_id' : encoded_channel_1['channel_id'],
        'u_id' : encoded_jwt_user2['u_id']
    }


    #user1 adds user2 as an owner to the channel
    requests.post(url + "/channel/addowner", json=addRemoveOwnerData)
    requests.post(url + "/channel/removeowner", json=addRemoveOwnerData)
    

    #assert that user2 is not part of channel1
    user_list_2 = requests.get(url + "channels/list", params={'token':encoded_jwt_user2['token']})
    user2_channels = user_list_2.json()
    
    assert user2_channels == {'channels' : []}
