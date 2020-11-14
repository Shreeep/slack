import time
from error import InputError, AccessError
import auth
import pytest
import other
import channels
import standup

def test_all_access_errors():
    other.clear()
    with pytest.raises(AccessError):
        standup.standup_start('token2', 1, 1)
    with pytest.raises(AccessError):
        standup.standup_active('token2', 1)
    with pytest.raises(AccessError):
        standup.standup_send('token2', 1, 'example')
    user1 = auth.auth_register('user12@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth.auth_register('user22@gmail.com', '123abc!@#', 'Bowen', 'Pierce')
    public_channel_id = channels.channels_create(user1['token'], "channel12", 1)['channel_id']
    with pytest.raises(AccessError):
        standup.standup_start(user2['token'], public_channel_id, 1)
    with pytest.raises(AccessError):
        standup.standup_active(user2['token'], public_channel_id)
    with pytest.raises(AccessError):
        standup.standup_send(user2['token'], public_channel_id, 'example')

def test_all_input_errors():
    other.clear()
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        standup.standup_start(user1['token'], 1, 1)
    with pytest.raises(InputError):
        standup.standup_active(user1['token'], 1)
    with pytest.raises(InputError):
        standup.standup_send(user1['token'], 1, 'example')
    public_channel_id = channels.channels_create(user1['token'], "channel12", 1)['channel_id']
    with pytest.raises(InputError):
        standup.standup_send(user1['token'], public_channel_id, 'y')
    with pytest.raises(InputError):
        standup.standup_send(user1['token'], public_channel_id, "y" * 1001)
    standup.standup_start(user1['token'], public_channel_id, 10)
    with pytest.raises(InputError):
        standup.standup_start(user1['token'], public_channel_id, 10)

def test_normal_use():
    other.clear()
    user1 = auth.auth_register('user13@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    public_channel_id = channels.channels_create(user1['token'], "channel12", 1)['channel_id']
    assert standup.standup_start(user1['token'], public_channel_id, 3)['time_finish'] == standup.standup_active(user1['token'], public_channel_id)['time_finish']
    assert standup.standup_active(user1['token'], public_channel_id)['is_active']
    standup.standup_send(user1['token'], public_channel_id, 'testt')
    standup.standup_send(user1['token'], public_channel_id, 'testt')
    time.sleep(3)
    assert not standup.standup_active(user1['token'], public_channel_id)['is_active']
