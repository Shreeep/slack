import auth
import user
import pytest
import other
from error import InputError, AccessError

def test_all_access_errors():
    other.clear()
    with pytest.raises(AccessError):
        other.users_all('token2')
    with pytest.raises(AccessError):
        other.admin_userpermission_change('token2', 1, 1)
    with pytest.raises(AccessError):
        other.search('token2', 'example')