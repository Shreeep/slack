import pytest
import re
from error import AccessError, InputError
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from datetime import datetime, timedelta

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
        'channel_id': payload_channel_one['channel_id'],
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'I am not in the channel but I still want to send a message'
    }

    result = requests.post(url + "/message/send", json=message_info)
    #Raises AccessError if User2 tries sending a message in a channel he is not apart of 
    assert result.status_code == 400

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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }

    message_two = {
        'token': payload_user1['token'],
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Oh no please remove this message'
    }
    requests.post(url + "/message/send", json=message_one)
    accidental_message = requests.post(url + "/message/send", json=message_two)
    result = accidental_message.json()
    deletion = requests.delete(url + "/message/remove", params={'token': payload_user1['token'], 'message_id': result['message_id']})
    assert deletion.status_code == 200

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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message_one = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message_one.json()
    requests.delete(url + "/message/remove", json={'token': payload_user1['token'], 'message_id': message_payload['message_id']})
    #Request to delete the message again after it has already been removed i.e. no longer exists - raise Input Error
    result = requests.delete(url + "/message/remove", json={'token': payload_user1['token'], 'message_id': message_payload['message_id']})
    assert result.status_code == 400

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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message.json()

    #User2 (who is not apart of the channel) trys to remove the message - AccessError
    r_1 = requests.delete(url + "/message/remove", json={'token':payload_user2['token'], 'message_id':message_payload['message_id']})
    assert r_1.status_code == 400

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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Hello this is user2, try remove my message user1'
    }
    send_message = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message.json()
    #User 1 Requesting to remove User 2's message since User 1 is the Owner - he should be allowed to do this 
    r_1 = requests.delete(url + "/message/remove", json={'token':payload_user1['token'], 'message_id':message_payload['message_id']})
    assert r_1.status_code == 200

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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message.json()
    #User2 (who is not apart of the channel) trys to edit the message - AccessError
    r_1 = requests.put(url + "/message/edit", json={'token':payload_user2['token'], 'message_id':message_payload['message_id'], 'message':'asdasd message ahha'})
    assert r_1.status_code == 400

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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Hello this is user2, try editing my message user1'
    }
    send_message = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message.json()
    #User 1 Requesting to edit User 2's message since User 1 is the Owner - he should be allowed to do this 
    r_1 = requests.put(url + "/message/edit", json={'token':payload_user1['token'], 'message_id':message_payload['message_id'], 'message':'asdasd message ahha'})
    assert r_1.status_code == 200

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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Unedited message'
    }
    send_message = requests.post(url + "/message/send", json=message_one)
    message_payload = send_message.json()
    #User 2 Requesting to edit their own message - should be allowed
    r_1 = requests.put(url + "/message/edit", json={'token':payload_user2['token'], 'message_id':message_payload['message_id'], 'message':'Edited message'})
    assert r_1.status_code == 200
    
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    result = requests.post(url + "/message/send", json=message_one)
    result_payload = result.json()
    r_1 = requests.put(url + "/message/edit", json={'token': payload_user1['token'], 'message_id': result_payload['message_id'], 'message': ''})
    assert r_1.status_code == 200
    
def test_post_message_react(url):
    # User info:
    user1 = {
        'email': 'twerwer@email.com',
        'password': 'password123',
        'name_first': 'Jen',
        'name_last': 'Bob'
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()
    successful_react =requests.post(url + "/message/react", json={'token':payload_user1['token'], 'message_id': result['message_id'], 'react_id': 1})
    assert successful_react.status_code == 200


def test_post_message_react_invalid_message_id(url):
    # User info:
    user1 = {
        'email': 'twerwer@email.com',
        'password': 'password123',
        'name_first': 'Jen',
        'name_last': 'Bob'
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()
    invalid_message_id_request = requests.post(url + "/message/react", json={'token':payload_user1['token'], 'message_id': result['message_id'] + 100, 'react_id': 1})
    assert invalid_message_id_request.status_code == 400

def test_post_message_react_invalid_react_id(url): 
    # User info:
    user1 = {
        'email': 'twerwer@email.com',
        'password': 'password123',
        'name_first': 'Jen',
        'name_last': 'Bob'
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()
    invalid_react_id_request = requests.post(url + "/message/react", json={'token':payload_user1['token'], 'message_id': result['message_id'], 'react_id': 3})
    assert invalid_react_id_request.status_code == 400

def test_post_message_react_already_reacted(url):
    # User info:
    user1 = {
        'email': 'twerwer@email.com',
        'password': 'password123',
        'name_first': 'Jen',
        'name_last': 'Bob'
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()
    requests.post(url + "/message/react", json={'token':payload_user1['token'], 'message_id': result['message_id'], 'react_id': 1})
    already_reacted_request = requests.post(url + "message/react", json={'token':payload_user1['token'], 'message_id': result['message_id'], 'react_id': 1})
    assert already_reacted_request.status_code == 400

def test_post_message_unreact(url):
    # User info:
    user1 = {
        'email': 'twerwer@email.com',
        'password': 'password123',
        'name_first': 'Jen',
        'name_last': 'Bob'
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()
    requests.post(url + "/message/react", json={'token':payload_user1['token'], 'message_id': result['message_id'], 'react_id': 1})
    successful_unreact = requests.post(url + "/message/unreact", json={'token':payload_user1['token'], 'message_id': result['message_id'], 'react_id': 0})
    assert successful_unreact.status_code == 200

def test_post_message_unreact_invalid_message_id(url):
    # User info:
    user1 = {
        'email': 'twerwer@email.com',
        'password': 'password123',
        'name_first': 'Jen',
        'name_last': 'Bob'
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()
    requests.post(url + "/message/react", json=result)
    invalid_unreact_message_id = requests.post(url + "/message/unreact", json={'token':payload_user1['token'], 'message_id': result['message_id'] + 100, 'react_id': 0})
    assert invalid_unreact_message_id.status_code == 400

def test_post_message_unreact_invalid_react_id(url):
    # User info:
    user1 = {
        'email': 'twerwer@email.com',
        'password': 'password123',
        'name_first': 'Jen',
        'name_last': 'Bob'
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()
    requests.post(url + "/message/react", json=result)
    invalid_react_id_request = requests.post(url + "/message/unreact", json={'token':payload_user1['token'], 'message_id': result['message_id'], 'react_id': 3})
    assert invalid_react_id_request.status_code == 400
 
def test_post_message_unreact_already_unreacted(url):
     # User info:
    user1 = {
        'email': 'twerwer@email.com',
        'password': 'password123',
        'name_first': 'Jen',
        'name_last': 'Bob'
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()
    requests.post(url + "/message/react", json={'token':payload_user1['token'], 'message_id': result['message_id'], 'react_id': 1})
    requests.post(url + "/message/unreact", json={'token':payload_user1['token'], 'message_id': result['message_id'], 'react_id': 0})
    already_unreacted = requests.post(url + "/message/unreact", json={'token':payload_user1['token'], 'message_id': result['message_id'], 'react_id': 0})
    assert already_unreacted.status_code == 400

def test_post_message_sendlater(url):
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
    current_time = datetime.utcnow()
    future_time = current_time + timedelta(seconds = 60) 
    send_message_later = requests.post(url + "/message/sendlater", json={'token': payload_user1['token'], 'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello',
        'time_sent': int(future_time.timestamp()),
    })
    assert send_message_later.status_code == 200

def test_post_message_sendlater_wrongtime(url): 
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
    current_time = datetime.utcnow()
    past_time = current_time - timedelta(seconds = 60) 
    send_message_later = requests.post(url + "/message/sendlater", json={'token': payload_user1['token'], 'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello',
        'time_sent': int(past_time.timestamp()),
    })
    assert send_message_later.status_code == 400

def test_message_pin_success(url):
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()

    message_pin_inputs = {
        'token' : payload_user1['token'],
        'message_id' : result['message_id']
    }

    pinned_message = requests.post(url + "/message/pin", json=message_pin_inputs)
    #success case
    assert pinned_message.status_code == 200

def test_message_pin_already_pinned(url):
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()

    message_pin_inputs = {
        'token' : payload_user1['token'],
        'message_id' : result['message_id']
    }
    pinned_message = requests.post(url + "/message/pin", json=message_pin_inputs)
    pinned_message = requests.post(url + "/message/pin", json=message_pin_inputs)

    #fails because InputError raised when already pinned
    assert pinned_message.status_code == 400

def test_message_unpin_success(url):
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()

    message_pin_inputs = {
        'token' : payload_user1['token'],
        'message_id' : result['message_id']
    }
    requests.post(url + "/message/pin", json=message_pin_inputs)
    unpinned_message = requests.post(url + "/message/unpin", json=message_pin_inputs)

    #fails because InputError raised when already pinned
    assert unpinned_message.status_code == 200

def test_message_unpin_already_unpinned(url):
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
        'channel_id': payload_channel_one['channel_id'],
        'message': 'Test Message Hello Hello'
    }
    send_message = requests.post(url + "/message/send", json=message_info)
    result = send_message.json()

    message_pin_inputs = {
        'token' : payload_user1['token'],
        'message_id' : result['message_id']
    }
    requests.post(url + "/message/pin", json=message_pin_inputs)
    requests.post(url + "/message/unpin", json=message_pin_inputs)
    unpinned_message = requests.post(url + "/message/unpin", json=message_pin_inputs)

    #fails because InputError raised when already unpinned
    assert unpinned_message.status_code == 400

