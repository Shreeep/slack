import requests
import json
# from echo_http_test import url
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
    dataIn = {
        'email': 'test@email.com',
        'password': 'password123',
        'name_first': 'test',
        'name_last': 'user'
    }

    r = requests.post(url + "/auth/register", json=dataIn)

    encoded_jwt = r.json()

    decoded_jwt = jwt.decode(encoded_jwt['token'], "secret string", algorithm='HS256')

    r = requests.get(url + "/user/profile", json=decoded_jwt)
    result = r.json()

    assert result['email'] == dataIn['email']
    assert result['name_first'] == dataIn['name_first']
    assert result['name_last'] == dataIn['name_last']



# def test_post_login(url):
#     dataIn = {
#         'email': 'test@email.com',
#         'password': 'password123',

#     }

#     r = requests.post(url + "/auth/login", json=dataIn)
#     user_token = r.json()
#     r = requests.get(url + "/user/profile", json=user_token)
#     result = r.json()
    
#     assert result['email'] == dataIn['email']
#     assert result['name_first'] == dataIn['name_first']
#     assert result['name_last'] == dataIn['name_last']


# def test_post_logout(url):

#     '''
#     Register user
#     Logout user
#     login with (expired) token
#     fail
#     '''
#     dataIn = {
#         'email': 'test@email.com',
#         'password': 'password123',
#         'name_first': 'test',
#         'name_last': 'user'
#     }

#     # register and login user
#     r = requests.post(url + "/auth/register", json=dataIn)

#     # return my u_id and token
#     user_token = r.json()

#     # log out with token
#     r = requests.post(url + "/auth/logout", json=user_token)

#     # successfully logged out
#     result = r.json()

#     assert result['is_success'] == True

#     # trying to log back in with previous token
#     # r = requests.get(url + "/user/profile", json=user_token)
#     # invalid = r.json()

