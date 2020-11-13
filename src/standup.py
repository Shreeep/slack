import threading
from datetime import timezone, datetime
import data
from message import message_send
from error import InputError, AccessError

def standup_start(token, channel_id, length):
    # check for valid token
    if not token in data.data['tokens']:
        raise AccessError
    # find user in token dictionary
    u_id = data.data['tokens'][token]
    # check if valid channel and user is member
    check_if_valid_channel(channel_id, u_id)
    # add member to channel if he is already not there
    date = datetime.now()
    timestamp = date.replace(tzinfo=timezone.utc).timestamp() + length
    start_time = threading.Timer(length, timer_over(token, channel_id))
    start_time.start()
    all_channels = data.data['channels']
    for channel in all_channels:
        if channel['id'] == channel_id:
            if channel['is_active']:
                raise InputError
            channel['is_active'] = True
            channel['time_finish'] = timestamp
            channel['standup_message'] = ''
    return {
        'time_finish': timestamp,
    }

def standup_active(token, channel_id):
    # check for valid token
    if not token in data.data['tokens']:
        raise AccessError
    # find user in token dictionary
    u_id = data.data['tokens'][token]
    # check if valid channel and user is member
    check_if_valid_channel(channel_id, u_id)
    # find channel and result it's details
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            result = {
                'is_active': channel['is_active'],
                'time_finish': None,
            }
            if channel['is_active']:
                result['time_finish'] = channel['time_finish']
            break
    return result

def standup_send(token, channel_id, message):
    # check for valid token
    if not token in data.data['tokens']:
        raise AccessError(description='wrong token')
    # check length of message restriction
    if len(message) > 1000:
        raise InputError
    # find user in token dictionary
    u_id = data.data['tokens'][token]
    # check if valid channel and user is member
    check_if_valid_channel(channel_id, u_id)
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            if not channel['is_active']:
                raise InputError
            if channel['standup_message'] != '':
                channel['standup_message'] += '\n'
            channel['standup_message'] += data.data['users'][u_id]['name_first'] + ': ' + message
    return {
    }

def timer_over(token, channel_id):
    all_channels = data.data['channels']
    for channel in all_channels:
        if channel['id'] == channel_id:
            message = channel['standup_message']
            channel['is_active'] = False
            channel['standup_message'] = ''
    message_send(token, channel_id, message)


def check_if_valid_channel(channel_id, u_id):
    # loop through channels to find channel with channel_id
    state = 0
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            # if u_id is not a member chuck an AccessError
            if not any(member['u_id'] == u_id for member in channel['members']):
                raise AccessError(description='not in channel')
            state = 1
    if state == 0:
        raise InputError(description='channel doesnt exist')
    