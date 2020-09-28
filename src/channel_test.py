import channel
import pytest
import data
from error import InputError

def test_channel_invite():
    channel.channel_invite("faweebawoowaba",123,456)

def test_channel_details():
    with pytest.raises(InputError) as e:
        assert echo.echo("echo")

def test_channel_messages():
    with pytest.raises(InputError) as e:
        assert echo.echo("echo")