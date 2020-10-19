import requests
import json
import auth_http
from echo_http_test import url


def test_post_register(url):
	dataIn = {
		'email': 'test@email.com',
		'password': 'password123',
		'name_first': 'Wilson',
		'name_last': 'Guo'
	}

    r = requests.post(url + "/auth/register", json=dataIn)
    user_token = r.json()
    r = requests.get(url + "/user/profile", json=user_token)
    result = r.json()

    assert result['email'] == dataIn['email']
    assert result['name_first'] == dataIn['name_first']
    assert result['name_last'] == dataIn['name_last']



def test_post_login(url):
	r = requests.post(url + "/login", json=dataIn)
	# result = r.json()
    pass



def test_post_logout(url):
	r = requests.post(url + "/logout", json=dataIn)
	# result = r.json()
    pass
