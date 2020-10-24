import pytest
import re
from error import AccessError, InputError
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

def test_post_message_send(url):
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
    message_info = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()
    assert result == {
        'message_id': result['message_id']
    }



def test_post_message_send_unauthorised(url):
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

    #Create a second user - that is NOT authorised to send messages to the channel 
    user2 = {
        'email': 'tqwert@email.com',
        'password': 'passwoqwerrd123',
        'name_first': 'gladys',
        'name_last': 'berejik'
    }
    register_user2 = requests.post(url + "/auth/register", json=user2)
    payload_user2 = register_user2.json()

    message_info = {
        'token': payload_user2['token'],
        'channel_id': payload_channel_one['id']
        'message': 'Test Message Hello Hello'
    }
    with pytest.raises(AccessError):
        requests.post(url + "/message/send", json=message_info)


def test_delete_message_remove(url):
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

    message_one = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['id'],
        'message': 'Test Message Hello Hello'
    }
    message_two = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['id'],
        'message': 'Oh no please remove this message'
    }
    message_payload = requests.post(url + "/message/send", json=message_one)
    requests.post(url + "/message/send", json=message_two)
    result = requests.delete(url + "/message/remove", json={'token': payload_user1['token'], 'message_id': message_payload['message_id']})
    assert result == {}


def test_delete_message_remove_no_longer_exists(url):
    #Remove a message
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

    message_one = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['id'],
        'message': 'Test Message Hello Hello'
    }
    message_two = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['id'],
        'message': 'Oh no please remove this message'
    }
    message_payload = requests.post(url + "/message/send", json=message_one)
    requests.post(url + "/message/send", json=message_two)
    result = requests.delete(url + "/message/remove", json={'token': payload_user1['token'], 'message_id': message_payload['message_id']})
    with pytest.raises(InputError):
        #Error raised since the message id does not exist as it was already removed
        #Therefore, if the remove request was called again - InputError 
        result = requests.delete(url + "/message/remove", json={'token': payload_user1['token'], 'message_id': message_payload['message_id']})

def test_delete_message_remove_unauthorised(url):

def test_delete_message_remove_owner_permission(url):

def test_put_message_edit_unauthorised(url):

def test_put_message_edit_owner_permission(url):

def test_put_message_edit_user_permission(url):

def test_put_message_edit_empty(url):

