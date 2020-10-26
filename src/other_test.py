import auth
import user
import pytest
import other
import channel
import channels
import message
from error import InputError, AccessError

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

def test_users_all():
    other.clear()
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register('user23@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    auth.auth_register('user33@gmail.com', '123abc!@#', 'Bowqween', 'Pierce')
    auth.auth_register('user43@gmail.com', '123abc!@#', 'Bowfqwen', 'Pierce')
    other.users_all(user1['token'])

def test_admin_userpermission_change():
    other.clear()
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user23@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    other.admin_userpermission_change(user1['token'], user2['u_id'], 1)

def test_search():
    other.clear()
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register('user23@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    public_channel_id = channels.channels_create(user1['token'], "channel16", 1)
    for i in range(60):
        message.message_send(user1['token'], public_channel_id['channel_id'], 'testing123')
        public_channel_id['channel_id'] = public_channel_id['channel_id'] + i - i
    other.search(user1['token'], 'testing123')
    other.search(user1['token'], 'testin5234')