import auth
import pytest

def test_register_fail():
	pass



def test_login_success():
	register1 = auth.auth_register("test@email.com", "password", "Wilson", "Guo")
	register2 = auth.auth_register("working@email.com", "workingPassword", "Test", "Name")
	assert auth.auth_login("test@email.com", "password") == {"u_id": 3, "token": 3}
	assert auth.auth_login("working@email.com", "workingPassword") == {"u_id": 4, "token": 4}


def test_login_fail():
	register1 = auth.auth_register("test@email.com", "password", "Wilson", "Guo")
	with pytest.raises(Exception) as e:
		auth.auth_login("wrong@email.com", "password") 
		auth.auth_login("test@email.com", "wrongpassword")
		auth.auth_login("notvalidemail", "password")
