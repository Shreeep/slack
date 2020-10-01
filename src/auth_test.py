import auth
import pytest
from error import InputError, AccessError

def test_login_success():
    register1 = auth.auth_register("test@email.com", "password", "Wilson", "Guo")
    register2 = auth.auth_register("working@email.com", "workingPassword", "Test", "Name")
    assert auth.auth_login("test@email.com", "password") == {"u_id": 3, "token": 3}
    assert auth.auth_login("working@email.com", "workingPassword") == {"u_id": 4, "token": 4}


def test_login_fail():
    register1 = auth.auth_register("test1@email.com", "password", "Wilson", "Guo")
    with pytest.raises(InputError) as e:
        assert auth.auth_login("wrong@email.com", "password") 

    with pytest.raises(InputError) as e:
        assert auth.auth_login("test1@email.com", "wrongpassword")

    with pytest.raises(InputError) as e:
        assert auth.auth_login("notvalidemail", "password")


def test_register_success():
    assert auth.auth_register("alreadyused@email.com", "password", "New", "Person") == {"u_id": 6, "token": 6}
    assert auth.auth_register("new@email.com", "newpassword", "Another", "Person") == {"u_id": 7, "token": 7}


def test_register_fail():
    with pytest.raises(InputError) as e:
        assert auth.auth_register("anotherinvalidemail", "password", "Register", "Fails")
        
    with pytest.raises(InputError) as e:
        auth.auth_register("alreadyused@email.com", "password", "Person", "Another")

    with pytest.raises(InputError) as e:
      assert auth.auth_register("shortpassword@email.com", "12345", "Short", "Password")

    with pytest.raises(InputError) as e:
      assert auth.auth_register("namelong@email.com", "password", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "surname")

    with pytest.raises(InputError) as e:
     assert  auth.auth_register("surnamelong@email.com", "password", "name", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
