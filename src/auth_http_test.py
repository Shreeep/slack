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




def test_post_register(url):
 
    # user info
    dataIn = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    # register user
    r = requests.post(url + "/auth/register", json=dataIn)
    encoded_jwt = r.json()

    # checking for valid token
    r = requests.get(url + "/users/all", params={'token': encoded_jwt['token']})
    result = r.json()

    user = result['users'][0]

    assert user['email'] == dataIn['email']
    assert user['name_first'] == dataIn['name_first']
    assert user['name_last'] == dataIn['name_last']


def test_post_logout(url):

    # user info
    dataIn = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    # register and login user
    r = requests.post(url + "/auth/register", json=dataIn)
    encoded_jwt = r.json()

    # log out with token
    r = requests.post(url + "/auth/logout", json=encoded_jwt)
    result = r.json()

    # successfully logged out
    assert result['is_success'] == True


def test_post_login(url):
   
    # user info
    dataIn = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    # register user
    r = requests.post(url + "/auth/register", json=dataIn)
    encoded_jwt = r.json()

    # log out with token
    r = requests.post(url + "/auth/logout", json=encoded_jwt)

    # user login info
    login_data = {
        'email': 'test@email.com',
        'password': 'password123',

    }

    # logging in
    r = requests.post(url + "/auth/login", json=login_data)
    encoded_jwt = r.json()

    # checking correct user
    r = requests.get(url + "/users/all", params={'token': encoded_jwt['token']})
    result = r.json()

    user = result['users'][0]
    
    assert user['email'] == dataIn['email']
    assert user['name_first'] == dataIn['name_first']
    assert user['name_last'] == dataIn['name_last']

def test_post_register_multiple(url):
    
    # user info
    dataIn = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    # register user
    r = requests.post(url + "/auth/register", json=dataIn)
    encoded_jwt = r.json()

    dataIn2 = {
        'email': 'test2@email.com',
        'password': 'password123456',
        'name_first': 'New',
        'name_last': 'User'
    }

    # register user
    r2 = requests.post(url + "/auth/register", json=dataIn2)
    encoded_jwt2 = r.json()

    # checking for valid token (user 1)
    r = requests.get(url + "/users/all", params={'token': encoded_jwt['token']})
    result = r.json()

    user = result['users'][0]

    assert user['email'] == dataIn['email']
    assert user['name_first'] == dataIn['name_first']
    assert user['name_last'] == dataIn['name_last']

    # checking for valid token (user 2)
    r2 = requests.get(url + "/users/all", params={'token': encoded_jwt2['token']})
    result = r.json()

    user = result['users'][1]

    assert user['email'] == dataIn2['email']
    assert user['name_first'] == dataIn2['name_first']
    assert user['name_last'] == dataIn2['name_last']

def test_post_logout_multiple(url):

    # user info
    dataIn = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    # register and login user
    r = requests.post(url + "/auth/register", json=dataIn)
    encoded_jwt = r.json()


    dataIn2 = {
        'email': 'test2@email.com',
        'password': 'password123456',
        'name_first': 'New',
        'name_last': 'User'
    }

    # register user 2
    r2 = requests.post(url + "/auth/register", json=dataIn2)
    encoded_jwt2 = r.json()

    # log out with token (user 1)
    r = requests.post(url + "/auth/logout", json=encoded_jwt)
    result = r.json()

    # successfully logged out
    assert result['is_success'] == True

    r2 = requests.post(url + "/auth/logout", json=encoded_jwt2)
    result2 = r.json()

    assert result2['is_success'] == True

def test_post_login_multiple(url):
   
    # user info
    dataIn = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    # register user 1
    r = requests.post(url + "/auth/register", json=dataIn)
    encoded_jwt = r.json()

    dataIn2 = {
        'email': 'test2@email.com',
        'password': 'password123456',
        'name_first': 'New',
        'name_last': 'User'
    }

    # register user 2
    r2 = requests.post(url + "/auth/register", json=dataIn2)
    encoded_jwt2 = r.json()

    # log out with token
    r = requests.post(url + "/auth/logout", json=encoded_jwt)
    r2 = requests.post(url + "/auth/logout", json=encoded_jwt2)

    # user login info
    login_data = {
        'email': 'test@email.com',
        'password': 'password123',

    }

    # logging in
    r = requests.post(url + "/auth/login", json=login_data)
    encoded_jwt = r.json()

    # checking correct user
    r = requests.get(url + "/users/all", params={'token': encoded_jwt['token']})
    result = r.json()

    user = result['users'][0]
    
    assert user['email'] == dataIn['email']
    assert user['name_first'] == dataIn['name_first']
    assert user['name_last'] == dataIn['name_last']

    login_data2 = {
        'email': 'test2@email.com',
        'password': 'password123456',

    }

    # logging in
    r2 = requests.post(url + "/auth/login", json=login_data2)
    encoded_jwt = r.json()

    # checking correct user
    r2 = requests.get(url + "/users/all", params={'token': encoded_jwt2['token']})
    result = r.json()
