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
        'is_public': True 
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
    assert result.status_code == 200

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
        'message': 'I am not in the channel but I still want to send a message'
    }

    result = requests.post(url + "/message/send", json=message_info)
    result_payload = result.json()
    #Raises AccessError if User2 tries sending a message in a channel he is not apart of 
    assert result_payload.status_code == 400

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
    requests.post(url + "/message/send", json=message_one)
    accidental_message = requests.post(url + "/message/send", json=message_two)
    result = accidental_message.json()
    r1 = requests.delete(url + "/message/remove", params={'token': payload_user1['token'], 'message_id': result['message_id']})
    r1_payload = r1.json()
    assert r1_payload.status_code == 200

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
    send_message_one = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message_one.json()
    deleted_message = requests.delete(url + "/message/remove", json={'token': payload_user1['token'], 'message_id': message_payload['message_id']})
    deleted_message_payload = deleted_message.json()
    result = requests.delete(url + "/message/remove", json={'token': payload_user1['token'], 'message_id': deleted_message_payload['message_id']})
    result_payload = result.json()
    assert result_payload.status_code == 400

def test_delete_message_remove_unauthorised(url):
    # User Info:
    user1 = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }
    # Register user:
    register_user1 = requests.post(url + "/auth/register", json=user1)
    payload_user1 = register_user1.json()
    
    #A second (unauthorised) user: 
    user2 = {
        'email': 'tqwert@email.com',
        'password': 'passwoqwerrd123',
        'name_first': 'gladys',
        'name_last': 'berejik'
    }
    register_user2 = requests.post(url + "/auth/register", json=user2)
    payload_user2 = register_user2.json()

    #Create channel associated with user1:
    test_channel_one_details = {
        'token': payload_user1['token'],
        'name': 'Public Channel #1',
        'is_public': True
    }
    create_channel_one = requests.post(url + "/channels/create", json=test_channel_one_details)
    payload_channel_one = create_channel_one.json()
    
    #User1 sends message
    message_one = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message.json()

    #User2 (who is not apart of the channel) trys to remove the message - AccessError
    r1 = requests.delete(url + "/message/remove", json={'token':payload_user2['token'], 'message_id':message_payload['message_id']})
    r1_payload = r1.json()
    assert r1_payload.status_code == 400

def test_delete_message_remove_owner_permission(url):
    # User Info:
    user1 = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }
    # Register user:
    register_user1 = requests.post(url + "/auth/register", json=user1)
    payload_user1 = register_user1.json()
    
    #A second (unauthorised) user: 
    user2 = {
        'email': 'tqwert@email.com',
        'password': 'passwoqwerrd123',
        'name_first': 'gladys',
        'name_last': 'berejik'
    }
    register_user2 = requests.post(url + "/auth/register", json=user2)
    payload_user2 = register_user2.json()

    #Create channel associated with user1:
    test_channel_one_details = {
        'token': payload_user1['token'],
        'name': 'Public Channel #1',
        'is_public': True
    }
    create_channel_one = requests.post(url + "/channels/create", json=test_channel_one_details)
    payload_channel_one = create_channel_one.json()

    #User 2 Joins channel and sends a message to it
    requests.post(url + "/channel/join", json={'token':payload_user2['token'], 'channel_id': payload_channel_one['channel_id']})

    #User2 sends message
    message_one = {
        'token': payload_user2['token'],
        'channel_id': payload_channel_one['id'],
        'message': 'Hello this is user2, try remove my message user1'
    }
    send_message = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message.json()
    #User 1 Requesting to remove User 2's message since User 1 is the Owner - he should be allowed to do this 
    r1 = requests.delete(url + "/message/remove", json={'token':payload_user1['token'], 'message_id':message_payload['message_id']})
    r1_payload = r1.json()
    assert r1_payload.status_code == 200

def test_put_message_edit_unauthorised(url):
    # User Info:
    user1 = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }
    # Register user:
    register_user1 = requests.post(url + "/auth/register", json=user1)
    payload_user1 = register_user1.json()
    
    #A second (unauthorised) user: 
    user2 = {
        'email': 'tqwert@email.com',
        'password': 'passwoqwerrd123',
        'name_first': 'gladys',
        'name_last': 'berejik'
    }
    register_user2 = requests.post(url + "/auth/register", json=user2)
    payload_user2 = register_user2.json()

    #Create channel associated with user1:
    test_channel_one_details = {
        'token': payload_user1['token'],
        'name': 'Public Channel #1',
        'is_public': True
    }
    create_channel_one = requests.post(url + "/channels/create", json=test_channel_one_details)
    payload_channel_one = create_channel_one.json()
    
    #User1 sends message
    message_one = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message.json()

    #User2 (who is not apart of the channel) trys to edit the message - AccessError
    r1 = requests.put(url + "/message/edit", json={'token':payload_user2['token'], 'message_id':message_payload['message_id'], 'message': 'blah blah poo poo bing'})
    r1_payload = r1.json()
    assert r1_payload.status_code == 400

def test_put_message_edit_owner_permission(url):
    # User Info:
    user1 = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }
    # Register user:
    register_user1 = requests.post(url + "/auth/register", json=user1)
    payload_user1 = register_user1.json()
    
    #A second user: 
    user2 = {
        'email': 'tqwert@email.com',
        'password': 'passwoqwerrd123',
        'name_first': 'gladys',
        'name_last': 'berejik'
    }
    register_user2 = requests.post(url + "/auth/register", json=user2)
    payload_user2 = register_user2.json()

    #Create channel associated with user1:
    test_channel_one_details = {
        'token': payload_user1['token'],
        'name': 'Public Channel #1',
        'is_public': True
    }
    create_channel_one = requests.post(url + "/channels/create", json=test_channel_one_details)
    payload_channel_one = create_channel_one.json()

    #User 2 Joins channel and sends a message to it
    requests.post(url + "/channel/join", json={'token':payload_user2['token'], 'channel_id': payload_channel_one['channel_id']})

    #User2 sends message
    message_one = {
        'token': payload_user2['token'],
        'channel_id': payload_channel_one['id'],
        'message': 'Hello this is user2, try editing my message user1'
    }
    send_message = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message.json()
    #User 1 Requesting to edit User 2's message since User 1 is the Owner - he should be allowed to do this 
    r1 = requests.put(url + "/message/edit", json={'token':payload_user1['token'], 'message_id':message_payload['message_id'], 'message':'asdasd message ahha'})
    r1_payload = r1.json()
    assert r1_payload.status_code == 200

def test_put_message_edit_user_permission(url):
    # User Info:
    user1 = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }
    # Register user:
    register_user1 = requests.post(url + "/auth/register", json=user1)
    payload_user1 = register_user1.json()
    
    #A second user: 
    user2 = {
        'email': 'tqwert@email.com',
        'password': 'passwoqwerrd123',
        'name_first': 'gladys',
        'name_last': 'berejik'
    }
    register_user2 = requests.post(url + "/auth/register", json=user2)
    payload_user2 = register_user2.json()

    #Create channel associated with user1:
    test_channel_one_details = {
        'token': payload_user1['token'],
        'name': 'Public Channel #1',
        'is_public': True
    }
    create_channel_one = requests.post(url + "/channels/create", json=test_channel_one_details)
    payload_channel_one = create_channel_one.json()

    #User 2 Joins channel and sends a message to it
    requests.post(url + "/channel/join", json={'token':payload_user2['token'], 'channel_id': payload_channel_one['channel_id']})

    #User2 sends message
    message_one = {
        'token': payload_user2['token'],
        'channel_id': payload_channel_one['id'],
        'message': 'Unedited message'
    }
    send_message = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message.json()
    #User 2 Requesting to edit their own message - should be allowed 
    r1 = requests.put(url + "/message/edit", json={'token':payload_user2['token'], 'message_id':message_payload['message_id'], 'message':'Edited message'})
    r1_payload = r1.json()
    assert r1_payload.status_code == 200
    
def test_put_message_edit_empty(url):
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
    requests.post(url + "/message/send", json=message_one)
    r1 = requests.put(url + "/message/edit", json={'token': payload_user1['token'], 'message_id': result['message_id'], 'message': ''})
    r1_payload = r1.json()
    assert r1_payload.status_code == 200
    



