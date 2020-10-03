import auth
import pytest
from other import clear
from error import InputError, AccessError

def test_register_success():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'Wilson', 'Guo')
    register2 = auth.auth_register('working@email.com', 'workingPassword', 'Test', 'Name')
    assert register1['u_id'] != None and register1['token'] != None
    assert register2['u_id'] != None and register2['token'] != None

def test_register_email_input_fail():
    clear()
    with pytest.raises(InputError) as e:
        assert auth.auth_register('anotherinvalidemail', 'password', 'Register', 'Fails')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('test@', 'password', 'Register', 'Fails')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('@.com', 'password', 'Register', 'Fails')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('!!##$$^^&@.com', 'password', 'Register', 'Fails')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('', 'password', 'Register', 'Fails')
        
def test_register_used_email_fail():
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('alreadyused@email.com', 'password', 'New', 'Person')
        assert auth.auth_register('alreadyused@email.com', 'password', 'Person', 'Another')

def test_register_password_length_fail():
    clear()
    with pytest.raises(InputError) as e:
        assert auth.auth_register('shortpassword@email.com', '12345', 'Short', 'Password')

def test_register_name_limit_fail():
    clear()
    with pytest.raises(InputError) as e:
        assert auth.auth_register('namelong@email.com', 'password', 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'surname')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('namelong@email.com', 'password', '', 'surname')

def test_register_surname_limit_fail():
    clear()
    with pytest.raises(InputError) as e:
        assert  auth.auth_register('surnamelong@email.com', 'password', 'name', 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')
        
    with pytest.raises(InputError) as e:
        assert  auth.auth_register('surnamelong@email.com', 'password', 'name', '')


def test_login_success():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'Wilson', 'Guo')
    register2 = auth.auth_register('working@email.com', 'workingPassword', 'Test', 'Name')
    login1 = auth.auth_login('test@email.com', 'password')
    login2 = auth.auth_login('working@email.com', 'workingPassword')
    assert login1['u_id'] == register1['u_id']
    assert login2['u_id'] == register2['u_id']

def test_login_fail():
    clear()
    auth.auth_register('test1@email.com', 'password', 'Wilson', 'Guo')
    with pytest.raises(InputError) as e:
        assert auth.auth_login('notvalidemail', 'password')

    with pytest.raises(InputError) as e:
        assert auth.auth_login('wrong@email.com', 'password') 

    with pytest.raises(InputError) as e:
        assert auth.auth_login('test1@email.com', 'wrongpassword')

def test_logout_success():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test2@email.com', 'password', 'test2', 'user2')
    assert auth.auth_logout(register1['token']) == {'is_success' : True}
    assert auth.auth_logout(register2['token']) == {'is_success' : True}


def test_logout_fail():
    clear()
    with pytest.raises(AccessError) as e:
        register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
        auth.auth_logout('invalidtoken')



