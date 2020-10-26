import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json


# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
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

def test_post_change_permission(url):
 
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

    # register users
    r = requests.post(url + "/auth/register", json=user_1_data)
    user_1 = r.json()

    r = requests.post(url + "/auth/register", json=user_2_data)
    user_2 = r.json()

    # create permission
    data_in = {
        'token': user_1['token'],
        'u_id': user_2['u_id'],
        'permission_id': 1
    } 
    requests.post(url + "/admin/userpermission/change", json=data_in)

    data_in = {
        'token': user_2['token'],
        'u_id': user_1['u_id'],
        'permission_id': 2
    }
    data_out = requests.post(url + "/admin/userpermission/change", json=data_in)
    result = data_out.json()
    # check no error code
    assert result == {}

def test_delete_clear(url):
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
    create_channel_one.json()
    # delete everything
    requests.delete(url + "/clear")
    # shouldnt be able to create channel anymore
    result = requests.post(url + "/channels/create", json=test_channel_one_details)
    assert result.status_code == 400


def test_get_search(url):
#tests if search http works

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

    messageData = {
        'token' : encoded_jwt_user1['token'],
        'channel_id' : channel_one['channel_id'],
        'message' : "testing123"
    }
    i = 0
    while i < 60:
        r = requests.post(url + "/message/send", json=messageData)
        i = i + 1

    queryData = {
        'token' : encoded_jwt_user1['token'],
        'query_str' : "testing123" 
    }

    falseQueryData = {
        'token' : encoded_jwt_user1['token'],
        'query_str' : "testin5234" 
    }

    r = requests.get(url + "/search", params=queryData)
    search_messages = r.json()

    r = requests.get(url + "/search", params=falseQueryData)
    search_nonexistent_messages = r.json()

    assert search_messages != {'messages': []}
    assert search_nonexistent_messages == {'messages': []}