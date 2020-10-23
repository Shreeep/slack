import auth
import user
import pytest
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

def test_user_profile_errors():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test', 'user')
    register3 = auth.auth_register('test2@email.com', 'password', 'test', 'user')

    # invalid u_id
    with pytest.raises(InputError):
        user.user_profile('token2', 10)

    # invalid token
    with pytest.raises(AccessError):
        user.user_profile('token8', 2)

def test_user_profile_setname():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test', 'user')
    register3 = auth.auth_register('test2@email.com', 'password', 'test', 'user')
    result = user.user_profile_setname('token2', 'New', 'UUSSSEEERRR')
    assert result == {}

def test_user_profile_setname_errors():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test', 'user')
    register3 = auth.auth_register('test2@email.com', 'password', 'test', 'user')

    # invalid first name length
    with pytest.raises(InputError):
        user.user_profile_setname('token2', '', 'lastname')

    # invalid first name length
    with pytest.raises(InputError):
        user.user_profile_setname('token2', 'abcdefghijklmnopqrstuvwyzabcdefghijklmnopqrstuvwyz', 'lastname')

    # invalid last name length
    with pytest.raises(InputError):
        user.user_profile_setname('token2', 'firstname', '')

    # invalid first name length
    with pytest.raises(InputError):
        user.user_profile_setname('token2', 'firstname', 'abcdefghijklmnopqrstuvwyzabcdefghijklmnopqrstuvwyz')


def test_user_profile_setemail():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test', 'user')
    register3 = auth.auth_register('test2@email.com', 'password', 'test', 'user')
    result = user.user_profile_setemail('token2', 'anewemail@email.com')
    assert result == {}

def test_user_profile_setemail_errors():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test', 'user')
    register3 = auth.auth_register('test2@email.com', 'password', 'test', 'user')

    # no @ symbol
    with pytest.raises(InputError):
        user.user_profile_setemail('token2', 'anewemailemail.com')

    # no .com
    with pytest.raises(InputError):
        user.user_profile_setemail('token2', 'anewemail@email')

    # no string before @
    with pytest.raises(InputError):
        user.user_profile_setemail('token2', '@email.com')

    # using symbols
    with pytest.raises(InputError):
        user.user_profile_setemail('token2', '!@#$%^@email.com')

    # no . after @ 
    with pytest.raises(InputError):
        user.user_profile_setemail('token2', 'anewemail@emailcom')

    # empty input
    with pytest.raises(InputError):
        user.user_profile_setemail('token2', '')

def test_user_profile_setemail_used():
    clear()
    auth.auth_register('test@email.com', 'password', 'New', 'Person')

    # used email
    with pytest.raises(InputError):
        user.user_profile_setemail('token1', 'test@email.com')
        
def test_user_profile_sethandle():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test', 'user')
    register3 = auth.auth_register('test2@email.com', 'password', 'test', 'user')
    result = user.user_profile_sethandle('token2', 'thisisanewhandle')
    assert result == {}

def test_user_profile_sethandle_errors():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test', 'user')
    register3 = auth.auth_register('test2@email.com', 'password', 'test', 'user')

    with pytest.raises(InputError):
        user.user_profile_sethandle('token2', 'ab')
