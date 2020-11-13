from datetime import timezone, datetime
import data
from error import InputError, AccessError
import auth
import user
import pytest
import other
import channel
import channels
import message
import standup

def test_all_access_errors():
    other.clear()
    with pytest.raises(AccessError):
        other.users_all('token2')
    with pytest.raises(AccessError):
        other.admin_userpermission_change('token2', 1, 1)
    with pytest.raises(AccessError):
        other.search('token2', 'example')
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user23@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    with pytest.raises(AccessError):
        other.admin_userpermission_change(user2['token'], user1['u_id'], 1)

def test_all_input_errors():
    other.clear()
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        other.admin_userpermission_change(user1['token'], user1['u_id'] + 25, 1)
    user2 = auth.auth_register('user23@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    with pytest.raises(InputError):
        other.admin_userpermission_change(user1['token'], user2['u_id'], 10)