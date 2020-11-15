import auth
import user
import pytest
from other import clear
from error import InputError, AccessError

def test_user_profile():
    clear()
    auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test1', 'user1')
    auth.auth_register('test2@email.com', 'password', 'test2', 'user2')
    result = user.user_profile(register2['token'], register2['u_id'])
    assert result == {
        'u_id': register2['u_id'],
        'email': 'test1@email.com',
        'name_first': 'test1',
        'name_last': 'user1',
        'handle_str': 'test1user1',
        'profile_img_url': '',
    }


def test_user_profile_errors():
    clear()
    auth.auth_register('test@email.com', 'password', 'test', 'user')
    auth.auth_register('test1@email.com', 'password', 'test1', 'user1')
    auth.auth_register('test2@email.com', 'password', 'test2', 'user2')

    # invalid u_id
    with pytest.raises(InputError):
        user.user_profile('token2', 10)

    # invalid token
    with pytest.raises(AccessError):
        user.user_profile('token8', 2)

    # valid token, but wrong u_id
    with pytest.raises(AccessError):
        user.user_profile('token2', 1)


def test_user_profile_setname():
    clear()
    auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test1', 'user1')
    auth.auth_register('test2@email.com', 'password', 'test2', 'user2')
    user.user_profile_setname(register2['token'], 'New', 'UUSSSEEERRR')
    user_profile = user.user_profile(register2['token'], register2['u_id'])

    assert user_profile == {
        'u_id': register2['u_id'],
        'email': 'test1@email.com',
        'name_first': 'New',
        'name_last': 'UUSSSEEERRR',
        'handle_str': 'test1user1',
        'profile_img_url': '',
    }


def test_user_profile_setname_errors():
    clear()
    auth.auth_register('test@email.com', 'password', 'test', 'user')
    auth.auth_register('test1@email.com', 'password', 'test1', 'user1')
    auth.auth_register('test2@email.com', 'password', 'test2', 'user2')

    # invalid first name length < 1
    with pytest.raises(InputError):
        user.user_profile_setname('token2', '', 'lastname')

    # invalid first name length > 50
    with pytest.raises(InputError):
        user.user_profile_setname('token2', 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'lastname')

    # invalid last name length < 1
    with pytest.raises(InputError):
        user.user_profile_setname('token2', 'firstname', '')

    # invalid first name length > 50
    with pytest.raises(InputError):
        user.user_profile_setname('token2', 'firstname', 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')
    
    with pytest.raises(AccessError):
        user.user_profile_setname('nbidsovno', 'testuser', '')


def test_user_profile_setemail():
    clear()
    auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test1', 'user1')
    auth.auth_register('test2@email.com', 'password', 'test2', 'user2')
    user.user_profile_setemail(register2['token'], 'anewemail@email.com')
    user_profile = user.user_profile(register2['token'], register2['u_id'])

    assert user_profile == {
        'u_id': register2['u_id'],
        'email': 'anewemail@email.com',
        'name_first': 'test1',
        'name_last': 'user1',
        'handle_str': 'test1user1',
        'profile_img_url': '',
    }


def test_user_profile_setemail_errors():
    clear()
    auth.auth_register('test@email.com', 'password', 'test', 'user')
    auth.auth_register('test1@email.com', 'password', 'test1', 'user1')
    auth.auth_register('test2@email.com', 'password', 'test2', 'user2')

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
    
    with pytest.raises(AccessError):
        user.user_profile_setemail('nbidsovno', 'testuser')


def test_user_profile_setemail_used():
    clear()
    auth.auth_register('test@email.com', 'password', 'New', 'Person')

    # used email
    with pytest.raises(InputError):
        user.user_profile_setemail('token1', 'test@email.com')


def test_user_profile_sethandle():
    clear()
    auth.auth_register('test@email.com', 'password', 'test', 'user')
    register2 = auth.auth_register('test1@email.com', 'password', 'test1', 'user1')
    auth.auth_register('test2@email.com', 'password', 'test2', 'user2')
    user.user_profile_sethandle(register2['token'], 'thisisanewhandle')
    user_profile = user.user_profile(register2['token'], register2['u_id'])

    assert user_profile == {
        'u_id': register2['u_id'],
        'email': 'test1@email.com',
        'name_first': 'test1',
        'name_last': 'user1',
        'handle_str': 'thisisanewhandle',
        'profile_img_url': '',
    }


def test_user_profile_sethandle_errors():
    clear()
    auth.auth_register('test@email.com', 'password', 'test', 'user')
    auth.auth_register('test1@email.com', 'password', 'test1', 'user1')
    auth.auth_register('test2@email.com', 'password', 'test2', 'user2')

    # invalid handle change < 3 
    with pytest.raises(InputError):
        user.user_profile_sethandle('token2', 'ab')

    # invalid handle change > 20
    with pytest.raises(InputError):
        user.user_profile_sethandle('token2', 'abcdefghijklmnopqrstuvwxyz')

    # handle used by another user
    with pytest.raises(InputError):
        user.user_profile_sethandle('token2', 'testuser')

    with pytest.raises(AccessError):
        user.user_profile_sethandle('nbidsovno', 'testuser')


def test_upload_photo_invalid_token():
    clear()
    auth.auth_register('test@email.com', 'password', 'test', 'user')

    with pytest.raises(AccessError):
        user.user_profile_upload_photo('invalidtoken', 'https://www.courant.com/resizer/D9qmAnzR8PY5q-GBdUBBVuNVUTs=/415x311/top/arc-anglerfish-arc2-prod-tronc.s3.amazonaws.com/public/NTWCZKYTDJBI7CASRJ32F2RN6E.jpg', 0, 0, 50, 50)


def test_upload_photo_status():
    clear()
    auth.auth_register('test@email.com', 'password', 'test', 'user')

    with pytest.raises(AccessError):
        user.user_profile_upload_photo('invalidtoken', 'img.jpg', 0, 0, 50, 50)


def test_upload_photo_not_jpg():
    clear()
    auth.auth_register('comp1531testuser@gmail.com', 'password', 'test', 'user')
    login1 = auth.auth_login('comp1531testuser@gmail.com', 'password')
    with pytest.raises(InputError):
        user.user_profile_upload_photo(login1['token'], 'img.png', 0, 0, 50, 50)

def test_upload_photo_success():
    clear()
    auth.auth_register('comp1531testuser@gmail.com', 'password', 'test', 'user')
    login1 = auth.auth_login('comp1531testuser@gmail.com', 'password')
    user.user_profile_upload_photo(login1['token'], 'https://upload.wikimedia.org/wikipedia/en/9/95/Test_image.jpg', 50, 50, 100, 100)
    
def test_upload_photo_x_too_small():
    clear()
    auth.auth_register('comp1531testuser@gmail.com', 'password', 'test', 'user')
    login1 = auth.auth_login('comp1531testuser@gmail.com', 'password')
    with pytest.raises(InputError):
        user.user_profile_upload_photo(login1['token'], 'https://upload.wikimedia.org/wikipedia/en/9/95/Test_image.jpg', -5, 50, 100, 100)
        
def test_upload_photo_y_too_small():
    clear()
    auth.auth_register('comp1531testuser@gmail.com', 'password', 'test', 'user')
    login1 = auth.auth_login('comp1531testuser@gmail.com', 'password')
    with pytest.raises(InputError):
        user.user_profile_upload_photo(login1['token'], 'https://upload.wikimedia.org/wikipedia/en/9/95/Test_image.jpg', 5, -50, 100, 100)

def test_upload_photo_x_end_too_small():
    clear()
    auth.auth_register('comp1531testuser@gmail.com', 'password', 'test', 'user')
    login1 = auth.auth_login('comp1531testuser@gmail.com', 'password')
    with pytest.raises(InputError):
        user.user_profile_upload_photo(login1['token'], 'https://upload.wikimedia.org/wikipedia/en/9/95/Test_image.jpg', 5, 50, -100, 100)
      
def test_upload_photo_y_end_too_small():
    clear()
    auth.auth_register('comp1531testuser@gmail.com', 'password', 'test', 'user')
    login1 = auth.auth_login('comp1531testuser@gmail.com', 'password')
    with pytest.raises(InputError):
        user.user_profile_upload_photo(login1['token'], 'https://upload.wikimedia.org/wikipedia/en/9/95/Test_image.jpg', 5, 50, 100, -100)
                          