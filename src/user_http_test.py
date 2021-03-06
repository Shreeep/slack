import requests
import json
import pytest
import re
import signal
import jwt
import hashlib
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


def test_user_profile(url):

    # user info
    data_in = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user',
    }

    # register user
    r = requests.post(url + "/auth/register", json=data_in)
    encoded_jwt = r.json()

    info = {
        'token': encoded_jwt['token'],
        'u_id': encoded_jwt['u_id']
    }

    # checking for valid token
    r = requests.get(url + "/user/profile", params=info)
    result = r.json()

    assert result['u_id'] == info['u_id']
    assert result['email'] == data_in['email']
    assert result['name_first'] == data_in['name_first']
    assert result['name_last'] == data_in['name_last']
    assert result['profile_img_url'] == ''

def test_user_profile_setname(url):
    
    # user info
    data_in = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user',
    }

    # register user
    r = requests.post(url + "/auth/register", json=data_in)
    encoded_jwt = r.json()

    info = {
        'token': encoded_jwt['token'],
        'name_first': 'NEWWWW',
        'name_last': 'USERRRR',
    }

    # check for valid token and change name
    r = requests.put(url + "/user/profile/setname", json=info)
    result = r.json()


    user_info = {
        'token': encoded_jwt['token'],
        'u_id': encoded_jwt['u_id']
    }

    # check it successfully changed
    r = requests.get(url + "/user/profile", params=user_info)
    result = r.json()

    assert result['u_id'] == user_info['u_id']
    assert result['email'] == data_in['email']
    assert result['name_first'] == info['name_first']
    assert result['name_last'] == info['name_last']
    assert result['profile_img_url'] == ''


def test_user_profile_setemail(url):
  
    # user info
    data_in = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user',
    }

    # register user
    r = requests.post(url + "/auth/register", json=data_in)
    encoded_jwt = r.json()

    info = {
        'token': encoded_jwt['token'],
        'email': 'new@email.com'
    }

    # check for valid token and change name
    r = requests.put(url + "/user/profile/setemail", json=info)
    result = r.json()

    user_info = {
        'token': encoded_jwt['token'],
        'u_id': encoded_jwt['u_id']
    }

    # check it successfully changed
    r = requests.get(url + "/user/profile", params=user_info)
    result = r.json()

    assert result['u_id'] == user_info['u_id']
    assert result['email'] == info['email']
    assert result['name_first'] == data_in['name_first']
    assert result['name_last'] == data_in['name_last']
    assert result['profile_img_url'] == ''


def test_user_profile_sethandle(url):
   
    # user info
    data_in = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user',
    }

    # register user
    r = requests.post(url + "/auth/register", json=data_in)
    encoded_jwt = r.json()

    info = {
        'token': encoded_jwt['token'],
        'handle_str': 'thisisanewhandle'
    }

    # check for valid token and change name
    r = requests.put(url + "/user/profile/sethandle", json=info)
    result = r.json()


    user_info = {
        'token': encoded_jwt['token'],
        'u_id': encoded_jwt['u_id']
    }

    # check it successfully changed
    r = requests.get(url + "/user/profile", params=user_info)
    result = r.json()

    assert result['u_id'] == user_info['u_id']
    assert result['email'] == data_in['email']
    assert result['name_first'] == data_in['name_first']
    assert result['name_last'] == data_in['name_last']
    assert result['profile_img_url'] == ''
    assert result['handle_str'] == info['handle_str']


def test_user_profile_error(url):

    # user info
    data_in = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user',
    }

    # register user
    r = requests.post(url + "/auth/register", json=data_in)

    new_token = jwt.encode({'token': 'anything'}, 'secret string', algorithm='HS256')

    # checking for valid token
    r = requests.get(url + "/user/profile", params=new_token)

    assert r.status_code == 400


def test_user_profile_setname_error(url):

    # user info
    data_in = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user',
    }

    # register user
    r = requests.post(url + "/auth/register", json=data_in)
    encoded_jwt = r.json()

    info = {
        'token': encoded_jwt['token'],
        'name_first': '',
        'name_last': 'user',
    }

    # checking for valid token
    r = requests.put(url + "/user/profile/setname", json=info)

    assert r.status_code == 400


def test_user_profile_setemail_error(url):

    # user info
    data_in = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user',
    }

    # register user
    r = requests.post(url + "/auth/register", json=data_in)
    encoded_jwt = r.json()

    info = {
        'token': encoded_jwt['token'],
        'email': 'wrongemail.com'
    }

    # checking for valid token
    r = requests.put(url + "/user/profile/setemail", json=info)

    assert r.status_code == 400


def test_user_profile_sethandle_error(url):

    # user info
    data_in = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user',
    }

    # register user
    r = requests.post(url + "/auth/register", json=data_in)
    encoded_jwt = r.json()

    info = {
        'token': encoded_jwt['token'],
        'handle_str': 'abcdefghijklmnopqrstuvwxyz'
    }

    # checking for valid token
    r = requests.put(url + "/user/profile/sethandle", json=info)

    assert r.status_code == 400


def test_user_profile_upload_photo_status(url):
    
    # user info
    data_in = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user',
    }

    # register user
    r = requests.post(url + "/auth/register", json=data_in)
    encoded_jwt = r.json()

    photo_info = {
        'token': encoded_jwt['token'],
        'img_url': 'https://www.courant.com/resizer/D9qmAnzR8PY5q-GBdUBBVuNVUTs=/415x311/top/arc-anglerfish-arc2-prod-tronc.s3.amazonaws.com/public/NTWCZKYTDJBI7CASRJ32F2RN6E.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 415,
        'y_end': 311,
    }
  
    requests.post(url + '/user/profile/uploadphoto', json=photo_info)

    profile_img = f"{photo_info['img_url']}{photo_info['x_start']}{photo_info['y_start']}{photo_info['x_end']}{photo_info['y_end']}{encoded_jwt['u_id']}"
    profile_img = hashlib.sha256(profile_img.encode()).hexdigest()[:10] + '.jpg'

    photo = requests.get(url + f'/static/{profile_img}')

    assert photo.status_code == 200

