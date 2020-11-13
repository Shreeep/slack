import auth
import pytest
from other import clear
from error import InputError, AccessError


def test_register_success():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'Wilson', 'Guo')
    register2 = auth.auth_register('working@email.com', 'workingPassword', 'Test', 'Name')
    auth.auth_register('test2@email.com', 'password', 'Wilson', 'Guo')
    assert register1['u_id'] != None and register1['token'] != None
    assert register2['u_id'] != None and register2['token'] != None

def test_register_email_input_fail():
    clear()
    # no @ symbol
    with pytest.raises(InputError):
        auth.auth_register('anotherinvalidemail', 'password', 'Register', 'Fails')

    # no .com
    with pytest.raises(InputError):
        auth.auth_register('test@', 'password', 'Register', 'Fails')

    # no string before @
    with pytest.raises(InputError):
        auth.auth_register('@.com', 'password', 'Register', 'Fails')

    # using symbols
    with pytest.raises(InputError):
        auth.auth_register('!!##$$^^&@.com', 'password', 'Register', 'Fails')

    # no . after @ 
    with pytest.raises(InputError):
        auth.auth_register('test@com', 'password', 'Register', 'Fails')

    # empty input
    with pytest.raises(InputError):
        auth.auth_register('', 'password', 'Register', 'Fails')
        
def test_register_used_email_fail():
    clear()
    # used email
    with pytest.raises(InputError):
        auth.auth_register('alreadyused@email.com', 'password', 'New', 'Person')
        auth.auth_register('alreadyused@email.com', 'password', 'Person', 'Another')

def test_register_password_length_fail():
    clear()
    # password limtation
    with pytest.raises(InputError):
        auth.auth_register('shortpassword@email.com', '12345', 'Short', 'Password')

def test_register_name_limit_fail():
    clear()
    # first name limitation
    with pytest.raises(InputError):
        auth.auth_register('namelong@email.com', 'password', 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'surname')

    with pytest.raises(InputError):
        auth.auth_register('namelong@email.com', 'password', '', 'surname')

def test_register_surname_limit_fail():
    clear()
    # surnname limitation
    with pytest.raises(InputError):
        auth.auth_register('surnamelong@email.com', 'password', 'name', 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')
        
    with pytest.raises(InputError):
        auth.auth_register('surnamelong@email.com', 'password', 'name', '')


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
    with pytest.raises(InputError):
        auth.auth_login('notvalidemail', 'password')

    with pytest.raises(InputError):
        auth.auth_login('wrong@email.com', 'password') 

    with pytest.raises(InputError):
        auth.auth_login('test1@email.com', 'wrongpassword')

def test_logout_success():
    clear()
    register1 = auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test2@email.com', 'password', 'test2', 'user2')
    assert auth.auth_logout(register1['token']) == {'is_success' : True}
    assert auth.auth_logout(register2['token']) == {'is_success' : True}


def test_logout_fail():
    clear()
    auth.auth_register('test@email.com', 'password', 'test', 'user')
    with pytest.raises(AccessError):
        auth.auth_logout('invalidtoken')


def test_passwordreset_success():
    clear()
    register1 = auth.auth_register('comp1531testuser@gmail.com', 'password', 'test', 'user')
    auth.auth_passwordreset_request('comp1531testuser@gmail.com')
    auth.auth_passwordreset_reset('d9515429f13ac55be806a691b61ce0a3f505d97517ae22da7e22f2f6bd92f986', 'newpassword')

    login1 = auth.auth_login('comp1531testuser@gmail.com', 'newpassword')
    
    assert login1['u_id'] == register1['u_id']


def test_passwordreset_old_pw_fail():
    clear()
    auth.auth_register('comp1531testuser@gmail.com', 'password', 'test', 'user')
    auth.auth_passwordreset_request('comp1531testuser@gmail.com')
    auth.auth_passwordreset_reset('d9515429f13ac55be806a691b61ce0a3f505d97517ae22da7e22f2f6bd92f986', 'newpassword')

    with pytest.raises(InputError):
        auth.auth_login('comp1531testuser@gmail.com', 'password')

def test_passwordreset_invalid_email():
    clear()
    auth.auth_register('comp1531testuser@gmail.com', 'password', 'test', 'user')
   
    with pytest.raises(InputError):
        auth.auth_passwordreset_request('test2email.com')


def test_passwordreset_invalid_code():
    clear()
    auth.auth_register('comp1531testuser@gmail.com', 'password', 'test', 'user')
    auth.auth_passwordreset_request('comp1531testuser@gmail.com')

    with pytest.raises(InputError):
        auth.auth_passwordreset_reset('', 'newpassword')


def test_passwordreset_invalid_password():
    clear()
    auth.auth_register('comp1531testuser@gmail.com', 'password', 'test', 'user')
    auth.auth_passwordreset_request('comp1531testuser@gmail.com')

    with pytest.raises(InputError):
        auth.auth_passwordreset_reset('comp1531testuser@gmail.compassword', '')    

