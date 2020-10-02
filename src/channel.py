import data
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    # check for valid token
    if not token in data.data['tokens']:
        raise AccessError
    # check for valid u_id
    if not u_id in data.data['users']:
        raise InputError
    # find target user and token user
    target_user = data.data['users'][u_id]
    user_id = data.data['tokens'][token]
    # find channel by channel_id
    check_if_valid_channel_and_member(channel_id, user_id)
    member_dict = {
        'u_id': u_id,
        'name_first': target_user['name_first'],
        'name_last': target_user['name_last'],
    }
    all_channels = data.data['channels']
    for channel in all_channels:
        if channel['id'] == channel_id:
            if not any(u_id == member['id'] for member in channel['members']): 
                channel['members'].append(member_dict)        
    return {
    }

def channel_details(token, channel_id):
    if not token in data.data['tokens']:
        raise AccessError
    u_id = data.data['tokens'][token]
    check_if_valid_channel_and_member(channel_id, u_id)
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            result = {
                'name': channel['name'],
                'owner_members': channel['owners'],
                'all_members': channel['members'],
            }
            break
    return result

def channel_messages(token, channel_id, start):
    if not token in data.data['tokens']:
        raise AccessError
    u_id = data.data['tokens'][token]
    check_if_valid_channel_and_member(channel_id, u_id)
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            messages = channel['messages']
            break
    span = 50
    result = []
    if start >= len(messages):
        raise InputError
    for i in range(span):
        index = i + start
        if index > len(messages) - 1:
            break
        result.append(messages[index])
    if (index - start) != 49:
        end = -1
    else:
        end = 50        
    return {
        'messages': result,
        'start': start,
        'end': end,
    }

def channel_leave(token, channel_id):
    return {
    }

def channel_join(token, channel_id):
    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }

def check_if_valid_channel_and_member(channel_id, u_id):
    for channel in data.data['channels']:
        if channel['id'] == channel_id:
            if not any(member['id'] == u_id for member in channel['members']):
                raise AccessError
            return
    raise InputError