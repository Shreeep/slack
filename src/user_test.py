import user
import pytest
import auth
from other import clear
from error import InputError, AccessError

def test_user_profile():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test', 'user')
    register3 = auth.auth_register('test2@email.com', 'password', 'test', 'user')
    result = user.user_profile('token2', 2)
    assert result == {
        'u_id': 2,
        'email': 'test1@email.com',
        'name_first': 'test',
        'name_last': 'user',
        'handle_str': 'testuser2',
    }

def test_user_profile_setname():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test', 'user')
    register3 = auth.auth_register('test2@email.com', 'password', 'test', 'user')
    result = user.user_profile_setname('token2', 'New', 'UUSSSEEERRR')
    assert result == {}

def test_user_profile_setemail():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test', 'user')
    register3 = auth.auth_register('test2@email.com', 'password', 'test', 'user')
    result = user.user_profile_setemail('token2', 'anewemail@email.com')
    assert result == {}

def test_user_profile_sethandle():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test', 'user')
    register3 = auth.auth_register('test2@email.com', 'password', 'test', 'user')
    result = user.user_profile_sethandle('token2', 'thisisanewhandle')
    assert result == {}
