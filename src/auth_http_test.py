import requests
import json
import auth_http
from echo_http_test import url


def test_post_register(url):
    dataIn = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    r = requests.post(url + "/auth/register", json=dataIn)
    user_token = r.json()
    r = requests.get(url + "/user/profile", json=user_token)
    result = r.json()

    assert result['email'] == dataIn['email']
    assert result['name_first'] == dataIn['name_first']
    assert result['name_last'] == dataIn['name_last']



def test_post_login(url):
    dataIn = {
        'email': 'test@email.com',
        'password': 'password123',

    }

    r = requests.post(url + "/auth/login", json=dataIn)
    user_token = r.json()
    r = requests.get(url + "/user/profile", json=user_token)
    result = r.json()
    
    assert result['email'] == dataIn['email']
    assert result['name_first'] == dataIn['name_first']
    assert result['name_last'] == dataIn['name_last']


def test_post_logout(url):

    '''
    Register user
    Logout user
    login with (expired) token
    fail
    '''
    dataIn = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    # register and login user
    r = requests.post(url + "/auth/register", json=dataIn)

    # return my u_id and token
    user_token = r.json()

    # log out with token
    r = requests.post(url + "/auth/logout", json=user_token)

    # successfully logged out
    result = r.json()

    assert result['is_success'] == True

    # trying to log back in with previous token
    # r = requests.get(url + "/user/profile", json=user_token)
    # invalid = r.json()

